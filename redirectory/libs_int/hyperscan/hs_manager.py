import hyperscan
from typing import Optional, Union, List, Tuple

from kubi_ecs_logger import Logger, Severity

from .search_context import SearchContext
from .hs_database import HsDatabase
from redirectory.libs_int.database import get_model_by_id
from redirectory.models import RedirectRule

HYPERSCAN_EXPRESSION_FLAGS = {
    'i': hyperscan.HS_FLAG_CASELESS,
    's': hyperscan.HS_FLAG_DOTALL,
    'm': hyperscan.HS_FLAG_MULTILINE,
    'H': hyperscan.HS_FLAG_SINGLEMATCH,
    'V': hyperscan.HS_FLAG_ALLOWEMPTY,
    'W': hyperscan.HS_FLAG_UCP,
    '8': hyperscan.HS_FLAG_UTF8,
    'P': hyperscan.HS_FLAG_PREFILTER,
    'L': hyperscan.HS_FLAG_SOM_LEFTMOST
}


class HsManager:
    __instance: 'HsManager' = None
    database: HsDatabase = None

    def __new__(cls):
        """
        This function converts the HsManager class into an abstract class also know
        as the singleton pattern.
        If there is already an existing instance it will be returned.
        If there is no instance already it is going to create one and store it in a variable
        for later use

        Returns:
            the one and only instance of the HsManger class
        """
        if cls.__instance is None:
            cls.__instance = super(HsManager, cls).__new__(cls)
            cls.__instance.database = HsDatabase()
        return cls.__instance

    def search(self, domain: str, path: str, is_test: bool = False) -> Optional[Union[list, dict]]:
        """
        Searches the two Hyperscan databases for the best match.
        First it searches the domains to find the right one. Then it combines
        the id of the domain with the path into a rule.
        The rule is searched again with the Rule Hyperscan database.

        Args:
            domain: the domain to search for
            path: the path to the domain to search for
            is_test: if set to true the function returns the two search context objects for the domain and rule

        Returns:
            None: if no match is found
            int: the id of the redirect rule
            dict: a dictionary with both the domain and rule search context objects for testing
        """
        assert self.database.is_loaded, "Hyperscan Database must be loaded before using search"
        domain_rule_map = {}
        rule_searches = []

        # Search domain
        domain_search_ctx = self.search_domain(domain, SearchContext(original=domain))
        # Return if none found
        if domain_search_ctx.is_empty() and not is_test:
            return None
        # Fill rule map if is test
        if is_test:
            for domain_id in domain_search_ctx.matched_ids:
                domain_rule_map[domain_id] = []

        # Search rule for every matched domain
        rule_search_ctx_list = []
        for domain_id in domain_search_ctx.matched_ids:
            rule = f"{domain_id}{path}"
            if is_test:
                rule_searches.append(rule)

            rule_search_ctx = self.search_rule(rule, SearchContext(original=rule))

            if not rule_search_ctx.is_empty():
                if is_test:
                    domain_rule_map[domain_id] = rule_search_ctx.matched_ids
                rule_search_ctx_list.append(rule_search_ctx)
        # Return if none found
        if not rule_search_ctx_list and not is_test:
            return None

        if is_test:
            return {
                "domain_search": domain_search_ctx.original,
                "rule_searches": rule_searches,
                "domain_rule_map": domain_rule_map
            }
        else:
            return self._get_ids_from_ctx(rule_search_ctx_list)

    def search_domain(self, domain: str, domain_search_ctx: SearchContext = None) -> Optional[SearchContext]:
        """
        Searches a domain in the hyperscan domain database.
        Creates a SearchContext object and runs a scan for the domain. Also handles
        a cancellation of the search which is a hyperscan error with error code -3.
        If the search doesn't find any matches a None is returned.
        If there are matches then a SearchContext object will be returned.

        Args:
            domain: the domain to search for
            domain_search_ctx: SearchContext to be passed to Hyperscan

        Returns:
            None or a SearchContext object
        """
        if domain_search_ctx is None:
            domain_search_ctx = SearchContext(original=domain)

        try:
            self.database.domain_db.scan(domain, self._match_event_handler, context=domain_search_ctx)
        except hyperscan.error as e:
            if self.get_error_code(e) != -3:
                raise e

        Logger() \
            .event(category="hyperscan", action="hyperscan domain search successful",
                   dataset=str(domain_search_ctx.matched_ids)) \
            .out(severity=Severity.DEBUG)

        return domain_search_ctx

    def search_rule(self, rule: str, rule_search_ctx: SearchContext = None) -> Optional[SearchContext]:
        """
        Searches a rule in the hyperscan rule database.
        Really similar to the search_domain() method.
        If the search doesn't find any matches a None is returned.
        If there are matches then a SearchContext object will be returned.

        Args:
            rule: the rule to search for. {domain_id}/{path}
            rule_search_ctx: SearchContext to be passed to Hyperscan

        Returns:
            None or SearchContext object
        """
        if rule_search_ctx is None:
            rule_search_ctx = SearchContext(original=rule)

        try:
            self.database.rules_db.scan(rule, self._match_event_handler, context=rule_search_ctx)
        except hyperscan.error as e:
            if self.get_error_code(e) != -3:
                raise e

        Logger() \
            .event(category="hyperscan", action="hyperscan rule search successful",
                   dataset=str(rule_search_ctx.matched_ids)) \
            .out(severity=Severity.DEBUG)

        return rule_search_ctx

    @staticmethod
    def get_error_code(error: hyperscan.error) -> int:
        """
        Hyperscan errors are differentiated by their message instead of an Exception object.
        This method extracts the error code of a Hyperscan error from the message of that error.

        Args:
            error: a Hyperscan error object

        Returns:
            integer representing the Hyperscan error
        """
        assert isinstance(error, hyperscan.error)
        arg = str(error).split(" ")[-1]
        return int(arg)

    @staticmethod
    def pick_result(db_session, redirect_rule_ids: list) -> Tuple[Optional[RedirectRule], Optional[bool]]:
        """
        Checks which of the redirect rules has the largest weight.
        Gets every redirect rule from the DB and compares their weights.
        If all the redirect rules have the same weight then the request
        is considered ambiguous

        Args:
            db_session: the database session to be used with all DB actions
            redirect_rule_ids: a list of all the redirect rule ids

        Returns:
            the picked redirect rule and if the choice is ambiguous or not
        """
        assert isinstance(redirect_rule_ids, list)

        if not redirect_rule_ids:
            return None, None

        weights = []
        heaviest_model: Optional[RedirectRule] = None

        for redirect_rule_id in redirect_rule_ids:
            redirect_rule: RedirectRule = get_model_by_id(db_session, RedirectRule, redirect_rule_id)
            weights.append(redirect_rule.weight)

            if heaviest_model is None:
                heaviest_model = redirect_rule
            elif redirect_rule.weight > heaviest_model.weight:
                heaviest_model = redirect_rule

        weights.sort(reverse=True)
        is_ambiguous = weights.count(weights[0]) > 1

        return heaviest_model, is_ambiguous

    @staticmethod
    def _match_event_handler(*args):
        """
        Function passed to Hyperscan library to handle events
        when a match is found. It makes use of the context which is passed
        as last argument.
        For more information about this function take a look at: _match_event_handler()
        from Hyperscan C library

        Args:
            *args:
                0: the id of the expression that matched
                1: from which index of the string the match starts
                2: until which index of the string the match ends
                3: the flags of the expression
                4: the context which is passed when running the scan

        Returns:
            True: if you want to stop scanning
            None: if you want to continue scanning
        """
        destination_id = args[0]
        from_index = args[1]
        to_index = args[2]
        ctx: SearchContext = args[4]

        ctx.handle_match(destination_id, from_index, to_index)

    @staticmethod
    def _get_ids_from_ctx(search_context_list: List[SearchContext]) -> list:
        """
        Takes a list of SearchContext objects and combines all the matched ids
        into a set to avoid duplicates and returns it converted in a list.

        Args:
            search_context_list: the list of SearchContext objects

        Returns:
            a list of unique matched ids
        """
        assert isinstance(search_context_list, list)
        final_ids = set()
        for search_context in search_context_list:
            for matched_id in search_context.matched_ids:
                final_ids.add(matched_id)

        return list(final_ids)
