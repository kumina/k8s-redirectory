"""
Endpoint: Management Test Request

Method: POST

RESPONSES:
    - 200: All the information gathered from the test run of the request
    - 400: Hyperscan database not loaded. Can't make search requests

The Test Request endpoint provides the ability to test a request on how it would
be process and redirect in a real world scenario. In the post data you specify the
request_url which will be ran just as a normal redirect from a worker would. The difference
is that not just the final redirect id is returned. A lot of data that might be useful for
debugging is exposed as well.

Steps:

    1. The request url is parsed and "host" and "path" are extracted from it
    2. The Hyperscan Manager is called to search but in test mode
    3. After the search is complete we convert all the IDs into their corresponding objects
    4. Everything is serialized and returned

For more information on how the search is done take a look at HsManager().search() function.

Good to test with:
    1. https://iirusa.com/epharmasummitwesta
    2. https://example.com/test/path
"""
from time import time
from typing import Tuple
from urllib.parse import urlparse

from flask import make_response, jsonify, request
from flask_restplus import Resource, fields
from kubi_ecs_logger import Logger, Severity

from redirectory.models import DomainRule, RedirectRule
from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.hyperscan import HsManager
from redirectory.libs_int.service import NamespaceManager, api_error
from redirectory.libs_int.database import DatabaseManager, get_model_by_id, db_encode_model

# Metrics
RULES_TEST_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

endpoint_args = api.model("test_request", {
    "request_url": fields.String(required=True, example="https://example.com/test/path"),
})


@api.route("/rules/test")
class ManagementTestRequest(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Test a request. What would be the response from the system.")
    @RULES_TEST_REQUEST_DURATION_SECONDS.time()
    def post(self):
        url = request.get_json()["request_url"]
        host, path = self.parse_url(url)

        # Init managers and sessions
        hs_manager = HsManager()
        db_session = DatabaseManager().get_session()

        # Search
        try:
            start_search_time = time()
            search_data = hs_manager.search(domain=host, path=path, is_test=True)
            end_search_time = time()
        except AssertionError as e:
            Logger() \
                .event(category="hyperscan", action="hyperscan search") \
                .error(message=str(e)) \
                .out(severity=Severity.ERROR)
            DatabaseManager().return_session(db_session)
            return api_error(
                message="Something went wrong during Hyperscan search!",
                errors=str(e),
                status_code=400
            )

        # Convert ids into models
        domain_rules_data = {}
        redirect_rules_data = {}
        d_r_map = search_data["domain_rule_map"]

        for domain_id in d_r_map.keys():
            domain_rule = get_model_by_id(db_session, DomainRule, domain_id)
            domain_rules_data[domain_id] = db_encode_model(domain_rule)

            for rule_id in d_r_map[domain_id]:
                redirect_rule = get_model_by_id(db_session, RedirectRule, rule_id)
                redirect_rules_data[rule_id] = db_encode_model(redirect_rule, expand=True)

        # Get final result
        final_redirect_rule, is_ambiguous = HsManager.pick_result(db_session, list(redirect_rules_data.keys()))

        # Fill in test data
        search_data["final_result_id"] = final_redirect_rule.id if final_redirect_rule is not None else None
        search_data["is_ambiguous"] = is_ambiguous
        search_data["time"] = str(end_search_time - start_search_time)

        DatabaseManager().return_session(db_session)
        return make_response(jsonify({
            "domain_rules": domain_rules_data,
            "redirect_rules": redirect_rules_data,
            "search_data": search_data
        }), 200)

    @staticmethod
    def parse_url(url: str) -> Tuple[str, str]:
        """
        Parses a url into a host and a path. Makes use of the
        built in urllib parser for urls

        Args:
            url: the whole url as a string

        Returns:
            a tuple containing the host and the path
        """
        url_obj = urlparse(url)
        host = url_obj.netloc
        host = host.split(":")[0]
        path = url_obj.path
        if url_obj.query != "":
            path += f"?{url_obj.query}"

        return host, path
