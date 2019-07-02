"""
Endpoint: Management Kubernetes Get Workers

Method: GET

RESPONSES:
    - 200: Returns a list of worker pods information
    - 400: Unable to get workers. Not running in a cluster

This endpoint provides the management pod with the ability to get
information about all of the worker pods. This is done with the use
of the Kubernetes API. It returns an array with every worker as an object.
If the application is not running in a Kubernetes environment then a 400 will be returned.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.kubernetes import K8sManager
from redirectory.libs_int.service import NamespaceManager, api_error

K8S_GET_WORKERS_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/kubernetes/get_workers")
class ManagementKubernetesGetWorkers(Resource):

    @api.doc(description="Get a list of all worker nodes currently up and running!")
    @K8S_GET_WORKERS_REQUEST_DURATION_SECONDS.time()
    def get(self):
        try:
            workers = K8sManager().get_worker_pods()
        except AssertionError as e:
            return api_error(
                message="Unable to get worker pods",
                errors=str(e),
                status_code=400
            )

        workers_data = []
        for worker in workers:
            workers_data.append(worker.get_data())

        return make_response(jsonify({
            "workers": workers_data,
            "status": "done"
        }), 200)
