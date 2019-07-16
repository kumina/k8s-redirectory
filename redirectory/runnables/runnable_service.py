from abc import ABC
from flask import Flask, request, Response

from kubi_ecs_logger import Logger, Severity

from .runnable import Runnable
from redirectory.libs_int.config import Configuration
from redirectory.libs_int.metrics import REQUESTS_TOTAL, start_metrics_server
from redirectory.libs_int.service import GunicornServer, Api
from redirectory.libs_int.database import DatabaseManager


class RunnableService(Runnable, ABC):
    api: Api = None
    application: Flask = None

    host: str = None
    port: int = None

    def __init__(self):
        super().__init__()

        self.api = Api(
            title="Redirectory",
            version="0.0.1",
            description="A service that is able to redirect urls that are usually going to end up as 404."
                        "You can configure the service how to redirect urls",
            doc="/redirectory-doc"
        )
        self.application = Flask(__name__)

        @self.application.after_request
        def _after_request(response: Response):
            """
            Logs every request that has been processed by the application.
            Logs Prometheus metrics for every request except for the status updates. (health and readiness checks)

            Args:
                response: the response to be returned

            Returns:
                the unmodified response
            """
            config = Configuration().values

            Logger() \
                .event(category="requests", action="request received") \
                .url(path=request.path, domain=request.host) \
                .source(ip=request.remote_addr) \
                .http_response(status_code=response.status_code) \
                .out(severity=Severity.INFO)

            if "status" not in request.path:
                REQUESTS_TOTAL.labels(config.node_type, str(response.status_code)).inc()

            return response

        self.host = self.config.service.ip
        self.port = self.config.service.port

    def _run_development(self):
        DatabaseManager().create_db_tables()

        Logger() \
            .event(category="runnable", action="run development") \
            .server(ip=self.host, port=self.port) \
            .out(severity=Severity.INFO)

        # CORS only in development
        @self.application.after_request
        def _after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Max-Age', 21600)
            return response

        # Start metric server
        start_metrics_server()

        # Run application
        self.application.run(**{
            "host": self.host,
            "port": self.port,
            "debug": True,
            "use_reloader": False
        })

    def _run_production(self, is_worker: bool = False):
        DatabaseManager().create_db_tables()

        service_options = {
            "bind": f"{self.host}:{self.port}",
            "loglevel": "critical",
            "worker_class": "gthread",
            "threads": 2 if is_worker else 10
        }

        Logger() \
            .event(category="runnable", action="run production",) \
            .server(ip=self.host, port=self.port) \
            .out(severity=Severity.INFO)

        # Run application
        GunicornServer(self.application, service_options).run()

    def _run_test(self):
        self._run_development()
