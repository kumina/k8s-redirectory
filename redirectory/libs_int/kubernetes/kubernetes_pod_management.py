import io
import zipfile
from typing import Optional

import requests
from requests.exceptions import ConnectionError

from .kubernetes_pod import Pod

MANAGEMENT_HS_DB_VERSIONS_ENDPOINT = "/management/database/version"
"""The endpoint for getting the up to date Hyperscan Database versions"""
MANAGEMENT_SYNC_DOWNLOAD_ENDPOINT = "/management/sync/download"
"""The endpoint for downloading all needed files to sync workers"""
MANAGEMENT_ADD_AMBIGUOUS = "/management/ambiguous/add"
"""The endpoint for adding an ambiguous request to the management pod db"""
MANAGEMENT_RELOAD_HS_DB = "/management/database/reload_management"
"""The endpoint for reloading the management pod hs DB for testing and from compiler job"""


class ManagementPod(Pod):

    def __init__(self, name: str, ip: str, port: int):
        super().__init__(name, ip, port)

    def get_data(self) -> dict:
        """
        Gathers all of the data about the management pod into a dict mainly
        for the user interface

        Returns:
            dictionary later to be converted to json
        """
        return {
            "pod": {
                "name": self.name,
                "ip": self.ip,
                "port": self.port
            },
            "status": {
                "configuration": self.get_configuration(),
                "health": self.get_status_health(),
                "ready": self.get_status_ready()
            },
            "hyperscan": {
                "db_version": self.get_hyperscan_db_version()
            }
        }

    def get_hyperscan_db_version(self) -> dict:
        """
        Makes a request and retrieves the real up to date version of the Hyperscan database
        from the management pod.

        Returns:
            dict:
                current_version: The version of the Hyperscan DB that needs to be used
                old_version: The previous version of the Hyperscan DB
        """
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_HS_DB_VERSIONS_ENDPOINT}"
            response = requests.get(url).json()
            return {
                "current_version": response["current_version"],
                "old_version": response["old_version"],
                "loaded_version": response["loaded_version"]
            }
        except ConnectionError:
            return {}

    def get_sync_zip_file(self) -> Optional[zipfile.ZipFile]:
        """
        Makes a request to the management pod which downloads the zip file that contains
        the sql database and the two hyperscan databases. Then converts it to a in memory zip file.

        Returns:
            zipfile object or None if something goes wrong
        """
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_SYNC_DOWNLOAD_ENDPOINT}"
            response = requests.get(url)
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            return zip_file
        except ConnectionError:
            return None

    def add_ambiguous_request(self, request_url) -> bool:
        """
        Sends a request to the management pod to add a new ambiguous request entry

        Args:
            request_url: the url for the entry ambiguous request entry itself

        Returns:
            if it added the entry or not
        """
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_ADD_AMBIGUOUS}"
            post_data = {
                "request": request_url
            }
            response = requests.post(url, json=post_data)
            return response.status_code == 200
        except ConnectionError:
            return False

    def reload_hs_db(self) -> bool:
        """
        Sends a request to the management pod to reload it's hs db

        Returns:
            if it reloaded the database or not
        """
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_RELOAD_HS_DB}"
            response = requests.get(url)
            return response.status_code == 200
        except ConnectionError:
            return False
