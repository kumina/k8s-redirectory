"""
Endpoint: Management Add Ambiguous

Method: POST

RESPONSES:
    - 200: The ambiguous entry has been added
    - 400: An ambiguous entry like this already exists

The Add Ambiguous endpoint provides the ability to add an ambiguous entry
to the sqlite database.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, add_ambiguous_request, db_encode_model
from redirectory.libs_int.service import NamespaceManager, api_error

AMBIGUOUS_ADD_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("add_ambiguous", {
    "request": fields.String(required=True, example="https://example.com/request")
})


@api.route("/ambiguous/add")
class ManagementAddAmbiguous(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Add a new ambiguous request entry to the database")
    @AMBIGUOUS_ADD_REQUEST_DURATION_SECONDS.time()
    def post(self):
        new_request_url = request.get_json()["request"]
        db_session = DatabaseManager().get_session()

        # Delete the ambiguous entry and get bool if successful
        new_entry = add_ambiguous_request(db_session, new_request_url)

        # Release session
        DatabaseManager().return_session(db_session)

        if new_entry is not None:
            return make_response(jsonify({
                "new_ambiguous_request": db_encode_model(new_entry),
                "status": "done"
            }), 200)
        else:
            return api_error(
                message="Unable to add new ambiguous request entry",
                errors=f"Ambiguous request like this already exist",
                status_code=400
            )
