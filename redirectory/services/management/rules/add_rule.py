"""
Endpoint: Management Add Rule

Method: POST

RESPONSES:
    - 200: A new rule successfully added to the Redirect Rule database
    - 400: A Redirect Rule like this already exists

The Add Rule endpoint provides the ability to create/add new rule to the Redirect Rule database.
While creating the new Redirect Rule it checks if the rule already exists. If it does a 404 is returned.
If the Redirect Rule is new then it will be added to the database and a serialized JSON of the new
Redirect Rule instance will be returned.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, db_encode_model, add_redirect_rule
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
RULES_ADD_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("add_rule", {
    "domain": fields.String(required=True, example="test.com"),
    "domain_is_regex": fields.Boolean(required=True, example=False, default=False),
    "path": fields.String(required=True, example="/test/path"),
    "path_is_regex": fields.Boolean(required=True, example=False, default=False),
    "destination": fields.String(required=True, example="newtest.com/test/newpath"),
    "destination_is_rewrite": fields.Boolean(required=True, example=False, default=False),
    "weight": fields.Integer(required=True, example=100)
})


@api.route("/rules/add")
class ManagementAddRule(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Adds a rule to the database from the given args in the post data")
    @RULES_ADD_REQUEST_DURATION_SECONDS.time()
    def post(self):
        args = request.get_json()
        db_session = DatabaseManager().get_session()

        redirect_rule_instance = add_redirect_rule(db_session, **args)
        if redirect_rule_instance:
            redirect_rule_data = db_encode_model(redirect_rule_instance, expand=True)

            DatabaseManager().return_session(db_session)
            return make_response(jsonify({
                "new_rule": redirect_rule_data,
                "status": "done"
            }), 200)
        else:
            DatabaseManager().return_session(db_session)
            return api_error(
                message="Unable to add redirect rule",
                errors="A rule like this already exists",
                status_code=400
            )
