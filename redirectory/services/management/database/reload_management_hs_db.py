"""
Endpoint: Management Reload Hyperscan Database

Method: GET

RESPONSES:
    - 200: The Hyperscan Database has been reloaded

This endpoint provides the management pod with the ability to reload it's
hyperscan database that it uses for testing purposes.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.hyperscan import HsManager
from redirectory.libs_int.service import NamespaceManager

DATABASE_RELOAD_MANAGEMENT_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/database/reload_management")
class ManagementReloadManagementHsDb(Resource):

    @api.doc(description="Reload Management Hyperscan Test Database")
    @DATABASE_RELOAD_MANAGEMENT_REQUEST_DURATION_SECONDS.time()
    def get(self):
        hs_manager = HsManager()
        hs_manager.database.reload_database()
        new_db_version = hs_manager.database.db_version

        return make_response(jsonify({
            "new_hs_db_version": new_db_version,
            "status": "done"
        }), 200)

