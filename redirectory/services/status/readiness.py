"""
Endpoint: Status Readiness

Method: GET

RESPONSES:
    - 200: Service is up and running with a loaded Hyperscan DB
    - 400: Service is running but not ready yet. No Hyperscan DB loaded yet

This endpoints acts as a Readiness check for Kubernetes.
If the node is of type management then it will always be ready.
For management pod the Hyperscan Database doesn't matter. It is used only for testing.
If the Hyperscan Database is loaded then the Node can server requests and
therefor it is ready.
If the Hyperscan Database is NOT loaded yet then the Node is not ready to
server requests.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.config import Configuration
from redirectory.libs_int.service import NamespaceManager, api_error
from redirectory.libs_int.hyperscan import HsManager

# Metrics
STATUS_READY_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("status")


@api.route("/readiness_check")
class ServiceReadiness(Resource):

    @api.doc(description="Check if the current worker/management pod is ready for operations")
    @STATUS_READY_REQUEST_DURATION_SECONDS.time()
    def get(self):
        config = Configuration().values
        is_management = config.node_type == "management"

        if HsManager().database.is_loaded or is_management:
            return make_response(jsonify({
                "status": "ready"
            }), 200)
        else:
            return api_error(
                message="Not Ready",
                errors="Hyperscan database not loaded yet!",
                status_code=400
            )
