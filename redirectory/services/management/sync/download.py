"""
Endpoint: Management Sync Download

Method: GET

RESPONSES:
    - 200: Returns a zip file containing all needed files to perform a sync
    - 400: Something went wrong during processing of request. See error message.

This endpoint provides the management pod with the ability for worker pods
to download all of the three needed files in one as a zip.

Files in zip:

1. sqlite database
2. hyperscan domain database
3. hyperscan rule database
"""
from flask import send_file
from flask_restplus import Resource
from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.sync import Synchronizer
from redirectory.libs_int.service import NamespaceManager, api_error

# Metrics
SYNC_DOWNLOAD_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")

# Api Namespace
api = NamespaceManager().get_namespace("management")


@api.route("/sync/download")
class ManagementSyncDownload(Resource):

    @api.doc(description="Download all of the needed files in one as a zip")
    @SYNC_DOWNLOAD_REQUEST_DURATION_SECONDS.time()
    def get(self):
        sync = Synchronizer()

        try:
            zip_sync_file = sync.util_get_sync_files_as_zip()
        except FileNotFoundError as e:
            Logger() \
                .event(category="sync", action="sync download failed",
                       dataset="File not found while compressing into zip") \
                .error(message=str(e)) \
                .out(severity=Severity.ERROR)
            return api_error(
                message="Unable to gather needed files",
                errors="Some file/s needed for syncing is/are not available. "
                       "If the error persist contact the administrator",
                status_code=400
            )

        return send_file(zip_sync_file,
                         mimetype='zip',
                         attachment_filename="sync.zip",
                         as_attachment=True)
