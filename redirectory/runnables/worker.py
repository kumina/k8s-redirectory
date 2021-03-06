from kubi_ecs_logger import Logger, Severity

from .runnable_service import RunnableService
from redirectory.libs_int.hyperscan import HsManager
from redirectory.libs_int.service import NamespaceManager


class WorkerService(RunnableService):

    def run(self):
        HsManager().database.load_database()

        # Add the redirect
        from redirectory.services import WorkerRedirect
        self.api.add_resource(WorkerRedirect, "/", "/<path:content>")

        # Get needed namespaces
        worker_ns = NamespaceManager().get_namespace("worker")
        status_ns = NamespaceManager().get_namespace("status")

        # Add namespaces to api
        self.api.add_namespace(worker_ns)
        self.api.add_namespace(status_ns)

        # Init api with application
        self.api.init_app(self.application)

        # Log
        Logger() \
            .event(category="runnable", action="service configured") \
            .service(name="worker").out(severity=Severity.INFO)

        # Run according to configuration
        if self.config.deployment == "prod":
            self._run_production(is_worker=True)
        elif self.config.deployment == "dev":
            self._run_development()
        elif self.config.deployment == "test":
            self._run_test()
