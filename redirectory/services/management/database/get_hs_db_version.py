"""
Endpoint: Management Get Hyperscan DB Version

Method: GET

RESPONSES:
    - 200: Returns the old_version and the current_version. If not versions are yet available then None

The Get Hyperscan DB Version endpoint provides with the ability to retrieve
the previous and the current Hyperscan DB Version which are stored in the database.
It will return None for both if there is still no entry about versions in the database.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.hyperscan import get_hs_db_version, HsManager
from redirectory.libs_int.service import NamespaceManager

DATABASE_GET_VERSION_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/database/version")
class ManagementGetDBVersion(Resource):

    @api.doc(description="Returns the previous and current Hyperscan database version")
    @DATABASE_GET_VERSION_REQUEST_DURATION_SECONDS.time()
    def get(self):
        old_version, current_version = get_hs_db_version()
        hs_db_version = HsManager().database.db_version

        return make_response(jsonify({
            "old_version": old_version,
            "current_version": current_version,
            "loaded_version": hs_db_version,
            "status": "done"
        }), 200)
