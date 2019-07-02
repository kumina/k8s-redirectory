from time import time
from threading import Thread

from kubi_ecs_logger import Logger, Severity

from .runnable import Runnable
from redirectory.libs_int.hyperscan import HsManager, update_hs_db_version, get_expressions_and_ids
from redirectory.models import DomainRule, RedirectRule


class CompilerJob(Runnable):

    done_callback_function: callable = None

    def __init__(self, done_callback_function: callable = None):
        """
        Constructor. Checks for correct type and assigns variable

        Args:
            done_callback_function: the function to call when job is done
        """
        super().__init__()
        assert callable(done_callback_function) or done_callback_function is None, \
            "The done_callback_function must be a callable object or None!"
        self.done_callback_function = done_callback_function

    def run(self):
        # Start timer
        start_compile_time = time()

        # Create two threads for the two dbs
        domain_db_thread = Thread(name="compile_domain_db_thread", target=self._compile_domain_db)
        rules_db_thread = Thread(name="compile_domain_db_thread", target=self._compile_rules_db)

        # Log
        Logger() \
            .event(category="runner", action="job starting") \
            .container(name="compiler").out(severity=Severity.INFO)

        # Start two threads for the two dbs
        domain_db_thread.start()
        rules_db_thread.start()

        # Wait for the compilation to be done
        domain_db_thread.join()
        rules_db_thread.join()

        # Save the new db to the disk
        HsManager().database.save_database()

        # Update the new db version of the database
        new_hs_db_version = update_hs_db_version()

        # End compile time
        end_compile_time = time()

        # Print time took for compiling
        Logger() \
            .event(category="hyperscan", action="hyperscan database compile time",
                   dataset=str(end_compile_time - start_compile_time)) \
            .out(severity=Severity.INFO)
        # Print new log
        Logger() \
            .event(category="hyperscan", action="hyperscan database new version",
                   dataset=new_hs_db_version) \
            .out(severity=Severity.INFO)
        # Log job done
        Logger() \
            .event(category="runner", action="job complete") \
            .container(name="compiler").out(severity=Severity.INFO)

        # Call the callback function
        if self.done_callback_function is not None:
            self.done_callback_function(new_hs_db_version)

    @staticmethod
    def _compile_domain_db():
        """
        Gets the domain expressions and ids into two lists sorted in the same way.
        With the help of the HsDatabase class compiles an in-memory Hyperscan database.
        """
        domain_expressions, domain_ids = get_expressions_and_ids(db_model=DomainRule,
                                                                 expression_path="rule",
                                                                 expression_regex_path="is_regex",
                                                                 id_path="id")
        HsManager().database.compile_domain_db(domain_expressions, domain_ids)

    @staticmethod
    def _compile_rules_db():
        """
        Gets the path/redirect_rule expressions and ids into two lists sorted in the same way.
        With the help of the HsDatabase class compiles an in-memory Hyperscan database.
        """
        path_expressions, path_ids = get_expressions_and_ids(db_model=RedirectRule,
                                                             expression_path="path_rule.rule",
                                                             expression_regex_path="path_rule.is_regex",
                                                             id_path="id",
                                                             combine_expr_with="domain_rule.id")
        HsManager().database.compile_rules_db(path_expressions, path_ids)

    def _run_production(self):
        pass

    def _run_development(self):
        pass

    def _run_test(self):
        pass
