"""
Endpoint: Management Database Reload Workers

Method: GET

RESPONSES:
    - 200: All workers have been updated
    - 400: Unable to update some or all workers. Look at errors

This endpoint provides the management pod with the ability to send an update
request to all of the worker pods that are currently running on the cluster.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.sync import Synchronizer
from redirectory.libs_int.kubernetes import K8sManager
from redirectory.libs_int.service import NamespaceManager, api_error

DATABASE_RELOAD_WORKERS_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/database/reload_workers")
class ManagementReloadWorkersHsDb(Resource):

    @api.doc(description="With the help of kubernetes api update every worker with new db.")
    @DATABASE_RELOAD_WORKERS_REQUEST_DURATION_SECONDS.time()
    def get(self):
        try:
            workers = K8sManager().get_worker_pods()
        except AssertionError as e:
            return api_error(
                message="Unable to get worker pods",
                errors=str(e),
                status_code=400
            )

        sync = Synchronizer()
        failed_workers = sync.management_update_workers(workers)

        if failed_workers is not None:
            errors = []
            for failed_worker in failed_workers:
                errors.append(f"{failed_worker.name} - {failed_worker.ip}:{failed_worker.port}")
            return api_error(
                message="Some or all workers are unreachable.",
                errors=errors,
                status_code=400
            )

        return make_response(jsonify({
            "message": "New hyperscan DB are updated on the workers",
            "status": "done"
        }), 200)
