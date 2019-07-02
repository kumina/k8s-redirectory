"""
Endpoint: Management Delete Rule

Method: POST

RESPONSES:
    - 200: A Redirect Rule with that id has been deleted successfully
    - 404: A Redirect Rule with that id does NOT exist

The Delete Rule endpoint provides the ability to delete a RedirectRule
from the database. It will not take effect for the Hyperscan database. That
must be recompiled. The endpoint takes one argument which is the id of the Redirect Rule.
If the rule is found it's delete() method will be executed. The delete is custom
and it will delete Domain Rules, Path Rules and Destination Rules if they are not
used by any other Redirect Rule. For more insights on the topic take a look at delete_redirect_rule() function.
If no Redirect Rule with the given id exists then a 404 will be returned.
"""
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, delete_redirect_rule
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
RULES_DELETE_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("del_rule", {
    "rule_id": fields.Integer(required=True, example=1, min=1)
})


@api.route("/rules/delete")
class ManagementDeleteRule(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Delete an already existing rule from the database")
    @RULES_DELETE_REQUEST_DURATION_SECONDS.time()
    def post(self):
        rule_id = request.get_json()["rule_id"]
        db_session = DatabaseManager().get_session()

        # Delete the rule and get bool if successful
        is_deleted = delete_redirect_rule(db_session, rule_id)

        # Release session
        DatabaseManager().return_session(db_session)

        if is_deleted:
            return make_response(jsonify({
                "status": "done"
            }), 200)
        else:
            return api_error(
                message="Unable to delete redirect rule",
                errors=f"Redirect rule with id: {rule_id} does not exist",
                status_code=404
            )
