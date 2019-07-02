from kubi_ecs_logger import Logger, Severity

from .runnable_service import RunnableService
from redirectory.libs_int.service import NamespaceManager
from redirectory.libs_int.hyperscan import HsManager


class ManagementService(RunnableService):

    def run(self):
        # Load hyperscan database because of test in UI
        HsManager().database.load_database()

        # Get needed namespaces
        management_ns = NamespaceManager().get_namespace("management")
        status_ns = NamespaceManager().get_namespace("status")

        # Add the ui
        from redirectory.services import ManagementUI
        self.api.add_resource(ManagementUI, "/", "/<path:path>")

        # Log ui folder
        Logger().event(
            category="ui",
            action="ui loaded",
            dataset=self.config.directories.ui
        ).out(severity=Severity.INFO)

        # Add namespaces to api
        self.api.add_namespace(management_ns)
        self.api.add_namespace(status_ns)

        # Init api with application
        self.api.init_app(self.application)

        # Log
        Logger() \
            .event(category="runnable", action="service configured") \
            .service(name="management").out(severity=Severity.INFO)

        # Run according to configuration
        if self.config.deployment == "prod":
            self._run_production()
        elif self.config.deployment == "dev":
            self._run_development()
        elif self.config.deployment == "test":
            self._run_test()
