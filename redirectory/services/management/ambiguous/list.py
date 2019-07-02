"""
Endpoint: Management List Ambiguous

Method: GET

RESPONSES:
    - 200: A list of all ambiguous request entries
    - 404: No ambiguous entries in the SQL database

The List Ambiguous endpoint provides the ability to list all
currently stored ambiguous request entries in the SQL database.
"""
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, list_ambiguous_requests
from redirectory.libs_int.service import NamespaceManager, api_error

AMBIGUOUS_LIST_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/ambiguous/list")
class ManagementListAmbiguous(Resource):

    @api.doc(description="List all ambiguous request entries")
    @AMBIGUOUS_LIST_REQUEST_DURATION_SECONDS.time()
    def get(self):
        db_session = DatabaseManager().get_session()

        data = list_ambiguous_requests(db_session)

        DatabaseManager().return_session(db_session)
        if len(data) > 0:
            return make_response(jsonify({
                "ambiguous_requests": data,
                "status": "done"
            }), 200)
        else:
            return api_error(
                message="Unable to get ambiguous request entries",
                errors="No ambiguous entries in the SQL db",
                status_code=404
            )
