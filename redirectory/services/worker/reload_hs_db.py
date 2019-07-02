"""
Endpoint: Worker Reload Hyperscan Database

Method: GET

RESPONSES:
    - 200: A thread has started with the task of reloading the Hyperscan database

The Reload Hyperscan Database endpoint provides with the ability to start a thread
with the task of reloading the Hyperscan Database. The main is the Hyperscan Database but
also the SQL database is reloaded as well. When the thread starts it find the management
pod with the help of the Kubernetes API and downloads a zip file from it containing all
the needed file to reload itself. The zip file is then extracted and first the SQL manager
is reloaded and after that the Hyperscan database
"""
from threading import Thread

from flask import make_response, jsonify
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.sync import Synchronizer
from redirectory.libs_int.service import NamespaceManager

# Metrics
WORKER_RELOAD_HS_DB_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("worker")

# Api Namespace
api = NamespaceManager().get_namespace("worker")


@api.route("/reload_hs_db")
class WorkerReloadHsDb(Resource):

    @api.doc(description="Tells the current worker to update itself. Runs in a separate thread")
    @WORKER_RELOAD_HS_DB_REQUEST_DURATION_SECONDS.time()
    def get(self):
        sync = Synchronizer()

        sync_thread = Thread(name="sync worker thread", target=sync.worker_sync_files)
        sync_thread.start()

        return make_response(jsonify({
            "message": "Worker has started updating.",
            "status": "done"
        }), 200)
