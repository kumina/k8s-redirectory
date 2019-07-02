"""
Endpoint: Management Database Reload Worker

Method: POST

RESPONSES:
    - 200: The specified worker has started updating
    - 400: Unable to update the specified worker. See errors

This endpoint provides the management pod with the ability to send an update
request to one specific the worker pod.
Before sending an update worker request to the worker the endpoint checks if
the worker actually exists by making a health status request.
If the health status request fails then the worker is considered unreachable and a 400 is returned.
If the health status request succeeds then a second reload worker hs db request is send.
If the reload worker hs db requests returns 200 then the worker has started updating itself.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields
from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.sync import Synchronizer
from redirectory.libs_int.kubernetes import WorkerPod
from redirectory.libs_int.service import NamespaceManager, api_error

DATABASE_RELOAD_WORKER_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("update_worker", {
    "name": fields.String(required=True, example="redirectory-worker"),
    "ip": fields.String(required=True, example="127.0.0.1"),
    "port": fields.Integer(required=True, example=8001),
})


@api.route("/database/reload_worker")
class ManagementReloadWorkerHsDb(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="With the help of kubernetes api update every worker with new db.")
    @DATABASE_RELOAD_WORKER_REQUEST_DURATION_SECONDS.time()
    def post(self):
        args = request.get_json()
        name = args["name"]
        ip = args["ip"]
        port = args["port"]

        worker_pod = WorkerPod(name=name, ip=ip, port=port)

        if not worker_pod.get_status_health():
            message = "Unable to update worker pod."
            error = f"Pod with name: {worker_pod.name} and address: {worker_pod.ip}:{worker_pod.port} " \
                    "is unreachable"
            Logger() \
                .event(category="request", action="request failed", dataset=message) \
                .error(message=error) \
                .out(severity=Severity.ERROR)

            return api_error(
                message=message,
                errors=error,
                status_code=400
            )

        sync = Synchronizer()
        did_sync_start = sync.management_update_worker(worker_pod)

        if not did_sync_start:
            message = "Unable to update worker pod"
            error = f"Pod with name: {worker_pod.name} and address: {worker_pod.ip}:{worker_pod.port} " \
                    f"is reachable but did not respond correctly to sync worker request"
            Logger() \
                .event(category="synchronizer", action="synchronizer request failed",
                       dataset=message) \
                .error(message=error) \
                .out(severity=Severity.ERROR)

            return api_error(
                message=message,
                errors=error,
                status_code=400
            )

        return make_response(jsonify({
            "message": f"New hyperscan DB is updated on the specified worker with address: {worker_pod.ip}:{worker_pod.port}",
            "status": "done"
        }), 200)
