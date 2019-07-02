"""
Endpoint: Management Update Rule

Method: POST

RESPONSES:
    - 200: The Redirect Rule with that id was successfully updated
    - 404: A Redirect Rule with that id does NOT exist

The Update Rule endpoint provides the ability to update the information for a given Redirect Rule in
the database. In the post data all of the needed information for the creation of a rule is specified including
the Redirect Rule ID which points to which rule you wish to update. If a Redirect Rule with that ID is not
found then a 404 is returned.
For more information on how the update rule process works take a look at update_redirect_rule() function.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.service import NamespaceManager, api_error
from redirectory.libs_int.database import DatabaseManager, update_redirect_rule, db_encode_model

# Metrics
RULES_UPDATE_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("update_rule", {
    "redirect_rule_id": fields.Integer(required=True, example=1),
    "domain": fields.String(required=True, example="test.com"),
    "domain_is_regex": fields.Boolean(required=True, example=False, default=False),
    "path": fields.String(required=True, example="/test/path"),
    "path_is_regex": fields.Boolean(required=True, example=False, default=False),
    "destination": fields.String(required=True, example="newtest.com/test/newpath"),
    "destination_is_rewrite": fields.Boolean(required=True, example=False, default=False),
    "weight": fields.Integer(required=True, example=100)
})


@api.route("/rules/update")
class ManagementUpdateRule(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Update a rule that already exists in the database")
    @RULES_UPDATE_REQUEST_DURATION_SECONDS.time()
    def post(self):
        args = request.get_json()
        db_session = DatabaseManager().get_session()

        updated_redirect_rule = update_redirect_rule(db_session, **args)

        if updated_redirect_rule:
            serialized_updated_redirect_rule = db_encode_model(updated_redirect_rule, expand=True)

            DatabaseManager().return_session(db_session)
            return make_response(jsonify({
                "updated_rule": serialized_updated_redirect_rule,
                "status": "done"
            }), 200)
        else:
            DatabaseManager().return_session(db_session)
            return api_error(
                message="Unable to update redirect rule",
                errors=f"Redirect rule with id: {args['redirect_rule_id']} does not exist",
                status_code=404
            )

