from typing import Optional

import requests
from requests.exceptions import ConnectionError

from .kubernetes_pod import Pod

WORKER_HS_DB_VERSION_ENDPOINT = '/worker/get_hs_db_version'
WORKER_RELOAD_HS_DB_ENDPOINT = '/worker/reload_hs_db'


class WorkerPod(Pod):

    def __init__(self, name: str, ip: str, port: int):
        super().__init__(name, ip, port)

    def get_data(self) -> dict:
        """
        Gathers all of the data about the worker pod into a dict mainly
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

    def get_hyperscan_db_version(self) -> Optional[str]:
        """
        Sends a request to the worker pod and gets the version of the hs db
        that is loaded on it

        Returns:
            the version of the hs db or None
        """
        try:
            url = f"http://{self.ip}:{self.port}{WORKER_HS_DB_VERSION_ENDPOINT}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()["hs_db_version"]
            return None
        except ConnectionError:
            return None

    def sync(self) -> bool:
        """
        Sends a request to the worker pod to reload it's hs db

        Returns:
            if it reloaded the database or not
        """
        try:
            url = f"http://{self.ip}:{self.port}{WORKER_RELOAD_HS_DB_ENDPOINT}"
            response = requests.get(url)
            return response.status_code == 200
        except ConnectionError:
            return False

