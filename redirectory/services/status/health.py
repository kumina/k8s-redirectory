"""
Endpoint: Status Health

Method: GET

RESPONSES:
    - 200: Service is up and running

A really simple endpoint that just returns a status OK.
Useful for Kubernetes to know if the service has started and it's
running. For more in depth check see the Status Readiness.
The endpoint returns the same no matter the Node Configuration.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.service import NamespaceManager

# Metrics
STATUS_HEALTH_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("status")


@api.route("/health_check")
class ServiceHealth(Resource):

    @api.doc(description="Get the status of the service")
    @STATUS_HEALTH_REQUEST_DURATION_SECONDS.time()
    def get(self):
        return make_response(jsonify({
            "status": "ok"
        }))
