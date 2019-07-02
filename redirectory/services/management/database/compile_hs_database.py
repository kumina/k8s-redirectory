"""
Endpoint: Management Compile Hyperscan Database

Method: GET

RESPONSES:
    - 200: Doesn't matter it will always return a done status
    - 400: Unable to compile new hyperscan database

The Compile Hyperscan Database endpoint provides you with the ability to
compile a new Hyperscan Database from the current SQLite3 database which holds all
the Redirect Rules.

TODO: Make it work with Jobs
"""
from threading import Thread
from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.models import RedirectRule
from redirectory.runnables import CompilerJob
from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.database import DatabaseManager, db_get_table_row_count
from redirectory.libs_int.sync import Synchronizer
from redirectory.libs_int.service import NamespaceManager, api_error


DATABASE_COMPILE_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")
api = NamespaceManager().get_namespace("management")


@api.route("/database/compile")
class ManagementCompileNewDb(Resource):

    @api.doc(description="Compile a new version of HS databases based on the sqlite DB")
    @DATABASE_COMPILE_REQUEST_DURATION_SECONDS.time()
    def get(self):
        db_session = DatabaseManager().get_session()
        sync = Synchronizer()

        # Check if you can compile empty db
        redirect_rule_table_row_count = db_get_table_row_count(db_session, RedirectRule)
        DatabaseManager().return_session(db_session)

        if redirect_rule_table_row_count == 0:
            return api_error(
                message="Unable to compile new Hyperscan database",
                errors=f"Can't compile new Hyperscan database from no Redirect rules stored in the SQL database",
                status_code=400
            )

        compiler = CompilerJob(sync.util_new_hs_db_version_callback)

        compile_thread = Thread(target=compiler.run)
        compile_thread.start()

        return make_response(jsonify({
            "message": "New hyperscan DB are compiled",
            "status": "done"
        }), 200)
