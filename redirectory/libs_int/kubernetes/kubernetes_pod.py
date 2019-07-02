import requests
from requests.exceptions import ConnectionError

STATUS_HEALTH_ENDPOINT: str = "/status/health_check"
"""The endpoint for getting the health status"""
STATUS_READY_ENDPOINT: str = "/status/readiness_check"
"""The endpoint for getting the readiness status"""
STATUS_CONFIGURATION_ENDPOINT: str = "/status/get_node_configuration"
"""The endpoint for getting the configuration of the pod"""


class Pod:
    """
    A class containing all common attributes and functions of all Pods
    This class is inherited by both WorkerPod and ManagementPod and provides
    common attributes. It also provides basic function for getting status and configurations.

    Attributes:
        name (str): the name of the pod in Kubernetes
        ip (str): the internal ip of the pod in the Kubernetes cluster
        port (str): the port on which the application inside the pod is listening
    """
    name: str = None
    ip: str = None
    port: int = None

    def __init__(self, name: str, ip: str, port: int):
        self.name = name
        self.ip = ip
        self.port = port

    def get_status_health(self) -> bool:
        """
        Makes a request to the pod with that ip and port and retrieves the
        health status of it.

        Returns:
            bool: is the pod healthy or not
        """
        try:
            url = f"http://{self.ip}:{self.port}{STATUS_HEALTH_ENDPOINT}"
            response = requests.get(url)
            return response.status_code == 200
        except ConnectionError:
            return False

    def get_status_ready(self) -> bool:
        """
        Makes a request to the pod with that ip and port and retrieves the
        ready status of it.

        Returns:
            bool: is the pod ready or not
        """
        try:
            url = f"http://{self.ip}:{self.port}{STATUS_READY_ENDPOINT}"
            response = requests.get(url)
            return response.status_code == 200
        except ConnectionError:
            return False

    def get_configuration(self) -> dict:
        """
        Makes a request to the pod with that ip and port and retrieves
        it's configuration in json format.

        Returns:
            dict: all of the configurations of the pod
        """
        try:
            url = f"http://{self.ip}:{self.port}{STATUS_CONFIGURATION_ENDPOINT}"
            response = requests.get(url)
            return response.json()["configuration"]
        except ConnectionError:
            return {}
