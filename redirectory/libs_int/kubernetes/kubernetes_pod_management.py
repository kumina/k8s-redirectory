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


class ManagementPod(Pod):

    def __init__(self, name: str, ip: str, port: int):
        super().__init__(name, ip, port)

    def get_data(self) -> dict:
        data = {
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
        return data

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
                "old_version": response["old_version"]
            }
        except ConnectionError:
            return {}

    def get_sync_zip_file(self) -> Optional[zipfile.ZipFile]:
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_SYNC_DOWNLOAD_ENDPOINT}"
            response = requests.get(url)
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            return zip_file
        except ConnectionError:
            return None

    def add_ambiguous_request(self, request_url) -> bool:
        try:
            url = f"http://{self.ip}:{self.port}{MANAGEMENT_ADD_AMBIGUOUS}"
            post_data = {
                "request": request_url
            }
            requests.post(url, json=post_data)
            return True
        except ConnectionError:
            return False
