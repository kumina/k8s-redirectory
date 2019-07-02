"""
Endpoint: Management Delete Ambiguous

Method: POST

RESPONSES:
    - 200: The ambiguous entry has been deleted
    - 404: An ambiguous entry with with this id does not exists

The Delete Ambiguous endpoint provides the ability to delete an ambiguous entry
from the sqlite database.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, delete_ambiguous_request
from redirectory.libs_int.service import NamespaceManager, api_error

AMBIGUOUS_DELETE_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("del_ambiguous", {
    "ambiguous_id": fields.Integer(required=True, example=1, min=1)
})


@api.route("/ambiguous/delete")
class ManagementDeleteAmbiguous(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Delete an already existing ambiguous entry from the database")
    @AMBIGUOUS_DELETE_REQUEST_DURATION_SECONDS.time()
    def post(self):
        ambiguous_id = request.get_json()["ambiguous_id"]
        db_session = DatabaseManager().get_session()

        # Delete the ambiguous entry and get bool if successful
        is_deleted = delete_ambiguous_request(db_session, ambiguous_id)

        # Release session
        DatabaseManager().return_session(db_session)

        if is_deleted:
            return make_response(jsonify({
                "status": "done"
            }), 200)
        else:
            return api_error(
                message="Unable to delete ambiguous request entry",
                errors=f"Ambiguous request with id: {ambiguous_id} does not exist",
                status_code=404
            )
