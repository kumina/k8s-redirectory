from prometheus_client import start_wsgi_server, REGISTRY, GC_COLLECTOR, Summary, Counter, Gauge

from kubi_ecs_logger import Logger, Severity
from redirectory.libs_int.config import Configuration

PREFIX = "redirectory"

# Request generic
REQUESTS_DURATION_SECONDS = Summary(
    name=f"{PREFIX}_requests_duration_seconds",
    documentation='Time spent processing requests',
    labelnames=("node_type",)
)
REQUESTS_TOTAL = Counter(
    name=f"{PREFIX}_requests_total",
    documentation="Number of requests processed",
    labelnames=("node_type", "code")  # code = [200, 301, 404 ..]
)

# Request redirects
REQUESTS_REDIRECTED_DURATION_SECONDS = Summary(
    name=f"{PREFIX}_requests_redirected_duration_seconds",
    documentation="Time spend processing a redirect request by label",
    labelnames=("node_type", "measure")  # measure = [total, hyperscan, db_lookup]
)
REQUESTS_REDIRECTED_TOTAL = Counter(
    name=f"{PREFIX}_requests_redirected_total",
    documentation="Number of requests that when processed were redirects by label",
    labelnames=("node_type", "code", "request_type")  # request_type = [normal, ambiguous, back_ref, not_found]
)

# Hyperscan database
HYPERSCAN_DB_COMPILED_TOTAL = Counter(
    name=f"{PREFIX}_hyperscan_db_compiled_total",
    documentation="Number of times the management pod has compiled the hyperscan db",
    labelnames=("node_type",)
)
HYPERSCAN_DB_RELOADED_TOTAL = Counter(
    name=f"{PREFIX}_hyperscan_db_reloaded_total",
    documentation="Number of times the worker pod has reloaded the hyperscan db",
    labelnames=("node_type",)
)
HYPERSCAN_DB_VERSION = Gauge(
    name=f"{PREFIX}_hyperscan_db_version",
    documentation="The version of the hyperscan database by node_type",
    labelnames=("node_type",)
)


def start_metrics_server():
    """
    Starts a http server on a port specified in the configuration file
    and exposes Prometheus metrics on it.
    Also removes GC_COLLECTOR metrics because they are not really needed.
    """
    # Remove garbage collection metrics
    REGISTRY.unregister(GC_COLLECTOR)

    # Gather configurations
    config = Configuration().values
    ip = config.service.ip
    metrics_port = config.service.metrics_port

    # Start server
    start_wsgi_server(metrics_port)

    # Log
    Logger() \
        .event(category="runnable", action="run metrics") \
        .server(ip=ip, port=metrics_port) \
        .out(severity=Severity.INFO)
