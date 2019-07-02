"""
Endpoint: Status Get Node Configuration

Method: GET

RESPONSES:
    - 200: The configuration as JSON is returned

The Status Get Node Configuration provides the ability to see the
configuration of the current Node. After the configuration is loaded
(which is one of the first things that the application does) it is in
dictionary form and is easily serializable to JSON and returned.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.config import Configuration
from redirectory.libs_int.service import NamespaceManager

# Metrics
STATUS_CONFIG_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("status")


@api.route("/get_node_configuration")
class ServiceGetConfiguration(Resource):

    @api.doc(description="Get the configuration of the service")
    @STATUS_CONFIG_REQUEST_DURATION_SECONDS.time()
    def get(self):
        config = Configuration().values

        return make_response(jsonify({
            "configuration": config
        }), 200)
