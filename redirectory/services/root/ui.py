"""
Endpoint: Management UI

Method: GET

RESPONSES:
    - 200: A file with that path exits and it is returned
    - 404: A file with that path doesn't exist

The Management UI endpoint serves the static html, css and js files that
are the UI itself. The path is the path to the file which the frontend requires.
If the path is None then the index.html will be served.
The UI static files are located in a folder specified in the Configuration of the node itself.
The endpoint serves files only from the specified folder.
If a file doesn't exists then a 404 is returned.
"""
import os
from flask import send_from_directory
from flask_restplus import Resource

from redirectory.libs_int.metrics import REQUESTS_DURATION_SECONDS
from redirectory.libs_int.config import Configuration
from redirectory.libs_int.service import api_error

# Metrics
UI_REQUEST_DURATION_SECONDS = REQUESTS_DURATION_SECONDS.labels("management")


class ManagementUI(Resource):

    @UI_REQUEST_DURATION_SECONDS.time()
    def get(self, path=None):
        if path is None:
            path = "index.html"

        ui_directory = Configuration().values.directories.ui
        does_file_exist = os.path.isfile(os.path.join(ui_directory, path))

        if does_file_exist:
            return send_from_directory(ui_directory, path)
        else:
            return api_error(
                message="Something went wrong!",
                errors="File not found",
                status_code=404
            )
