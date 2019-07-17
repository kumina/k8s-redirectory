"""
Endpoint: Worker Redirect

Method: GET

RESPONSES:
    - 301: A permanent redirect to the correct location
    - 404: Unable to find match for this request

The Worker Redirect endpoint is the CORE endpoint of the application.
It parses a request into a host and path. It conducts a search with the help
of the HsManager() on the host and path. The search returns a list of matched ids
of RedirectRules. If the list is larger than one then we pick the final match
with the help of HsManager.pick_result() function. If while picking the final result
there are two or more rules with the same weight then the request is considered
ambiguous and it is added to the Ambiguous Table. Also if the rewrite is not
configured correctly then a 404 page will be returned and the request will be also
added to the Ambiguous Table for later checking by a person.
"""
from typing import Optional

from flask import request, redirect
from flask_restplus import Resource
from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.hyperscan import HsManager
from redirectory.libs_int.database import DatabaseManager
from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS, REQUESTS_REDIRECTED_DURATION_SECONDS, \
    REQUESTS_REDIRECTED_TOTAL

# Metrics
REDIRECT_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("worker")
TOTAL_REQUESTS_REDIRECTED_DURATION_SECONDS = REQUESTS_REDIRECTED_DURATION_SECONDS.labels("worker", "total")
HYPERSCAN_REQUESTS_REDIRECTED_DURATION_SECONDS = REQUESTS_REDIRECTED_DURATION_SECONDS.labels("worker", "hyperscan")
DB_LOOKUP_REQUESTS_REDIRECTED_DURATION_SECONDS = REQUESTS_REDIRECTED_DURATION_SECONDS.labels("worker", "db_lookup")


class WorkerRedirect(Resource):

    @REDIRECT_REQUEST_DURATION_SECONDS.time()
    @TOTAL_REQUESTS_REDIRECTED_DURATION_SECONDS.time()
    def get(self, content=None):
        del content
        host = request.host.split(":")[0]
        path = request.path

        # Stop spamming for favicon pls
        if path == "/favicon.ico":
            self.page_404()

        # Init managers and sessions
        hs_manager = HsManager()
        db_session = DatabaseManager().get_session()

        # Search
        try:
            matching_ids = None
            with HYPERSCAN_REQUESTS_REDIRECTED_DURATION_SECONDS.time():  # Metric
                matching_ids = hs_manager.search(domain=host, path=path)

            is_404 = matching_ids is None
        except AssertionError as e:
            Logger() \
                .event(category="hyperscan", action="hyperscan search failed") \
                .error(message=str(e)) \
                .out(severity=Severity.ERROR)
            DatabaseManager().return_session(db_session)
            is_404 = True

        if is_404:
            REQUESTS_REDIRECTED_TOTAL.labels("worker", "404", "not_found").inc()
            self.page_404()

        # Get final result
        with DB_LOOKUP_REQUESTS_REDIRECTED_DURATION_SECONDS.time():  # Metric
            final_redirect_rule, is_ambiguous = HsManager.pick_result(db_session, list(matching_ids))
            final_destination_url = final_redirect_rule.destination_rule.destination_url
            is_back_ref: bool = final_redirect_rule.destination_rule.is_rewrite

        # Do back reference
        if is_back_ref:
            final_destination_url = self.apply_back_reference(path, final_redirect_rule)

        # Add ambiguous request to db if needed
        if is_ambiguous or final_destination_url is None:
            from redirectory.libs_int.kubernetes import K8sManager, ManagementPod

            try:
                management_pod: ManagementPod = K8sManager().get_management_pod()
                management_pod.add_ambiguous_request(request.url)
            except AssertionError as e:
                Logger() \
                    .event(category="sync", action="sync ambiguous request",
                           dataset="Unable to sync ambiguous request with the management pod") \
                    .error(message=str(e)) \
                    .out(severity=Severity.ERROR)

            if final_destination_url is None:
                self.page_404()

        # Sanitize final redirect url
        final_destination_url = self.sanitize_outgoing_redirect(final_destination_url)

        DatabaseManager().return_session(db_session)

        if is_ambiguous:
            REQUESTS_REDIRECTED_TOTAL.labels("worker", "301", "ambiguous").inc()
        elif is_back_ref:
            REQUESTS_REDIRECTED_TOTAL.labels("worker", "301", "back_ref").inc()
        else:
            REQUESTS_REDIRECTED_TOTAL.labels("worker", "301", "normal").inc()

        return redirect(final_destination_url, 301)

    @staticmethod
    def sanitize_outgoing_redirect(current_redirect: str) -> str:
        """
        If the url doesn't have a schema it will be added https.

        Args:
            current_redirect: the url to sanitize

        Returns:
            str which is the sanitized url
        """
        if current_redirect.startswith("http"):
            return current_redirect
        else:
            return f"https://{current_redirect}"

    @staticmethod
    def apply_back_reference(path: str, rule) -> Optional[str]:
        """
        If the destination rule is a rewrite rule then this function is responsible for
        creating the new destination url that has to be redirected to.
        It uses regex groups and string formatting from Python to achieve this.

        Args:
            host: the host of the incoming request
            path: the path of the incoming request
            rule: the rule that has matched for this request

        Returns:
            the final url to which the user should be redirected or None if it is configured wrong
        """
        import re
        import string

        try:
            # Get the rules from the Redirect rule obj
            path_rule: str = rule.path_rule.rule
            destination_rule: str = rule.destination_rule.destination_url

            # Extract all the groups and their values from the path
            r = re.compile(path_rule)
            groups_and_values = [m.groupdict() for m in r.finditer(path)][0]

            # Get all the variables that need to be replaced
            variables_to_replace = [tup[1] for tup in string.Formatter().parse(destination_rule) if tup[1] is not None]

            # Check and get all the needed vars to construct the final url
            replace_map = {}
            for var in variables_to_replace:
                if var in groups_and_values:
                    replace_map[var] = groups_and_values[var]

            # Replace all the placeholders with correct values
            destination_rule = destination_rule.format(**replace_map)

            return destination_rule
        except (KeyError, AttributeError, re.error):
            return None

    @staticmethod
    def page_404():
        from redirectory.libs_int.service import api_error

        return api_error(
            message="404 Page Not Found",
            errors="Hmm, the thing you are looking for is not here!",
            status_code=404
        )
