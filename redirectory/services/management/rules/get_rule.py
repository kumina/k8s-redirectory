"""
Endpoint: Management Get Rule

Method: POST

RESPONSES:
    - 200: A Redirect Rule with that ID exists and returned in serialized form
    - 404: A Redirect Rule with that id does NOT exist

The Get Rule endpoint provides the ability to retrieve a Redirect Rule by a given ID specified
in the post data of the request. If a Redirect Rule with that id doesn't exist then a 404 is returned.
If a rule with that id exist then it is serialized and returned.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.models import RedirectRule
from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, get_model_by_id, db_encode_model
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
RULES_GET_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("get_rule", {
    "rule_id": fields.Integer(required=True, example=1, min=1),
})


@api.route("/rules/get")
class ManagementGetRule(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Retrieve a rule from the database with a given ID")
    @RULES_GET_REQUEST_DURATION_SECONDS.time()
    def post(self):
        rule_id = request.get_json()["rule_id"]
        db_session = DatabaseManager().get_session()

        redirect_instance = get_model_by_id(db_session, RedirectRule, rule_id)

        if redirect_instance:
            redirect_rule_data = db_encode_model(redirect_instance, expand=True)

            DatabaseManager().return_session(db_session)
            return make_response(jsonify({
                "rule": redirect_rule_data,
                "status": "done"
            }), 200)
        else:
            DatabaseManager().return_session(db_session)
            return api_error(
                message="Unable to get redirect rule",
                errors=f"Redirect rule with id: {rule_id} do",
                status_code=404
            )
