"""
Endpoint: Worker Get Hyperscan DB Version

Method: GET

RESPONSES:
    - 200: Returns the current Hyperscan DB version that the worker is using
    - 400: The worker has not Hyperscan DB loaded at the moment

The Get Hyperscan DB Version endpoint provides with the ability to retrieve
the current Hyperscan DB Version that the HsManager() has loaded and is using to run queries.
If the worker still has not Hyperscan DB loaded then a 400 is returned.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_TOTAL, REQUESTS_DURATION_SECONDS
from redirectory.libs_int.hyperscan import HsManager
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
WORKER_GET_HS_DB_VERSION_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("worker")

# Api Namespace
api = NamespaceManager().get_namespace("worker")


@api.route("/get_hs_db_version")
class WorkerGetHsDbVersion(Resource):

    @api.doc(description="Get the current hyperscan database version that the worker is using")
    @WORKER_GET_HS_DB_VERSION_REQUEST_DURATION_SECONDS.time()
    def get(self):
        hs_db_version = HsManager().database.db_version
        if hs_db_version:
            return make_response(jsonify({
                "hs_db_version": hs_db_version
            }))
        else:
            return api_error(
                message="Worker has no Hyperscan Database loaded",
                errors=[],
                status_code=400
            )
