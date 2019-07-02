"""
Endpoint: Management Get Page

Method: POST

RESPONSES:
    - 200: A page of redirect rules has been successfully retrieved
    - 404: A page with that page number doesn't exists or there are no rule to paginate

The Get Page endpoint provides the ability to split up the RedirectRule
database into pages with a given size. From this endpoint you can retrieve
a given page by number with a given size.
The endpoint also accepts filters (optional) which will be applied and the result
of the filtered query will be paginated after that.
If no items are found with the specified filters then an api_error with error code 404
will be returned.
"""
from time import time
from flask import make_response, jsonify, request
from flask_restplus import Resource, fields

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.models import RedirectRule, DomainRule, PathRule, DestinationRule
from redirectory.libs_int.database import DatabaseManager, db_encode_model, paginate, Page, db_sanitize_like_query
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
RULES_GET_PAGE_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

# All possible filters to apply to the page selection
filter_args = api.model("filter", {
    "redirect_rule_id": fields.Integer(required=False, default=None),
    "domain_rule_id": fields.Integer(required=False, default=None),
    "path_rule_id": fields.Integer(required=False, default=None),
    "destination_rule_id": fields.Integer(required=False, default=None),
    "weight": fields.Integer(required=False, default=None),

    "domain": fields.String(required=False, example="example.com"),
    "domain_is_regex": fields.Boolean(default=False),
    "path": fields.String(required=False, example="/test/path"),
    "path_is_regex": fields.Boolean(default=False),
    "destination": fields.String(required=False, example="https://test.com/new/path"),
    "destination_is_rewrite": fields.Boolean(default=False),
})

# Page selection arguments
endpoint_args = api.model("get_page", {
    "page_number": fields.Integer(required=True, example=1, min=1),
    "page_size": fields.Integer(required=True, example=5, min=2),
    "filter": fields.Nested(filter_args, required=False)
})


@api.route("/rules/get_page")
class ManagementGetPage(Resource):

    @api.expect(endpoint_args, validate=True)
    @api.doc(description="Adds a rule to the database from the given args in the post data")
    @RULES_GET_PAGE_REQUEST_DURATION_SECONDS.time()
    def post(self):
        # Gather arguments
        args = request.get_json()
        page_number = args["page_number"]
        page_size = args["page_size"]

        # Get DB session
        db_session = DatabaseManager().get_session()

        start_process_time = time()
        # Generate query for pages
        query = db_session.query(RedirectRule)
        # Apply filters to query if needed
        if "filter" in args:
            query = self.apply_filters(query, args["filter"])

        # Get the page
        page: Page = paginate(query, page_number, page_size)

        # Check if page exists
        if not page.items:
            # Release the DB session and return an api error
            DatabaseManager().return_session(db_session)
            return api_error(
                message="Unable to get specified page",
                errors=f"Page with number: {page_number} does not exist",
                status_code=404
            )

        # Get the data in json
        data = []
        for redirect_rule in page.items:
            data.append(db_encode_model(redirect_rule, expand=True))
        end_process_time = time()

        # Return DB session and return response
        DatabaseManager().return_session(db_session)
        return make_response(jsonify({
            "data": data,
            "page": {
                "total_items": page.total,
                "total_pages": page.pages,
                "has_previous": page.has_previous,
                "has_next": page.has_next
            },
            "time": str(end_process_time - start_process_time)
        }), 200)

    @staticmethod
    def apply_filters(query, filters: dict):
        """
        Takes a query and a dict of filters. Checks if a given filter is in the
        dict and if so applies the corresponding filter to the query. Af the end
        the query will have a lot of "where" statements.

        Args:
            query: the query to add the filters to
            filters: all the filters as a dict

        Returns:
            the modified query
        """
        # ID and number filters
        if "redirect_rule_id" in filters:
            query = query.filter(RedirectRule.id == filters["redirect_rule_id"])
        if "domain_rule_id" in filters:
            query = query.filter(RedirectRule.domain_rule_id == filters["domain_rule_id"])
        if "path_rule_id" in filters:
            query = query.filter(RedirectRule.path_rule_id == filters["path_rule_id"])
        if "destination_rule_id" in filters:
            query = query.filter(RedirectRule.destination_rule_id == filters["destination_rule_id"])
        if "weight" in filters:
            query = query.filter(RedirectRule.weight == filters["weight"])

        # Booleans filters
        if "domain_is_regex" in filters:
            query = query.filter(RedirectRule.domain_rule.has(is_regex=filters["domain_is_regex"]))
        if "path_is_regex" in filters:
            query = query.filter(RedirectRule.path_rule.has(is_regex=filters["path_is_regex"]))
        if "destination_is_rewrite" in filters:
            query = query.filter(RedirectRule.destination_rule.has(is_rewrite=filters["destination_is_rewrite"]))

        # String filters
        if "domain" in filters:
            query_str = db_sanitize_like_query(filters["domain"])
            query = query.filter(RedirectRule.domain_rule.has(DomainRule.rule.like(query_str)))
        if "path" in filters:
            query_str = db_sanitize_like_query(filters["path"])
            query = query.filter(RedirectRule.path_rule.has(PathRule.rule.like(query_str)))
        if "destination" in filters:
            query_str = db_sanitize_like_query(filters["destination"])
            query = query.filter(RedirectRule.destination_rule.has(DestinationRule.destination_url.like(query_str)))

        return query
