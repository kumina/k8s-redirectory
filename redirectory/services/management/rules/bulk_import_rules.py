"""
Endpoint: Management Bulk Import Rules

Method: POST

RESPONSES:
    - 200: The import of the CSV file has started successfully
    - 400: Wrong file type or format of the CSV. Look at returned error message

The Bulk Import endpoint provides you with the ability to upload a CSV file
in a specific format in order to add a lot of Redirect Rules all at once.
The importing may take some time which depends on how large is the CSV file.
That is why the endpoint makes use of threads.
Before we pass the file to the thread we conduct some basic validation at first which includes:

1. Is the file of type CSV
2. Are all the columns specified in the file valid

After this validation has passed successfully then the file is handed over to tbe thread
and the import process starts.

Notes:

1. If duplicate Redirect Rules are encountered in the CSV file they will be ignored/skipped.
2. If there is a parsing error somewhere in the file then the whole import process fails
   and all of the so far added Redirect Rules to the DB are rolled back like nothing happened.
3. At the moment there is no way of telling if an import is finished.
"""
import threading
from flask import make_response, jsonify
from flask_restplus import Resource, reqparse
from werkzeug.datastructures import FileStorage

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS, metric_update_rules_total
from redirectory.libs_int.importers import CSVImporter
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
RULES_BULK_IMPORT_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")

file_upload_args = reqparse.RequestParser()
file_upload_args.add_argument("csv_file", type=FileStorage, location='files', required=True, help="CSV FILE")


@api.route("/rules/bulk_import")
class ManagementBulkImportRules(Resource):

    @api.expect(file_upload_args, validate=True)
    @api.doc(description="Adds a rule to the database from the given args in the post data")
    @RULES_BULK_IMPORT_REQUEST_DURATION_SECONDS.time()
    def post(self):
        args = file_upload_args.parse_args()
        csv_byte_file_in: FileStorage = args["csv_file"]

        try:
            csv_importer = CSVImporter(csv_byte_file_in)
        except AssertionError as e:
            return api_error(
                message="Failed file processing",
                errors=str(e),
                status_code=400
            )

        import_thread = threading.Thread(target=csv_importer.import_into_db)
        import_thread.start()

        # Metrics
        metric_update_rules_total()

        return make_response(jsonify({
            "status": "Import has been started. Rules will appear in DB when the import is complete."
        }), 200)
