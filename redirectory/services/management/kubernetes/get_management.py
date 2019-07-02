"""
Endpoint: Management Kubernetes Get Management

Method: GET

RESPONSES:
    - 200: Returns information about the management pod
    - 400: Unable to get management pod. Not running in a cluster

This endpoint provides the management pod with the ability to get
information about itself. This is done with the use of the Kubernetes API.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.kubernetes import K8sManager
from redirectory.libs_int.service import NamespaceManager, api_error

K8S_GET_MANAGEMENT_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/kubernetes/get_management")
class ManagementKubernetesGetManagement(Resource):

    @api.doc(description="Get data about the management pod!")
    @K8S_GET_MANAGEMENT_REQUEST_DURATION_SECONDS.time()
    def get(self):
        try:
            management_pod = K8sManager().get_management_pod()
        except AssertionError as e:
            return api_error(
                message="Unable to get management pod",
                errors=str(e),
                status_code=400
            )

        return make_response(jsonify({
            "management": management_pod.get_data(),
            "status": "done"
        }), 200)
