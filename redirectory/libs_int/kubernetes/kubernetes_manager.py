from typing import List, Optional
from kubernetes import client, config
from kubi_ecs_logger import Logger, Severity

from . import ManagementPod, WorkerPod
from redirectory.libs_int.config import Configuration


def get_port_by_name(port_list: list, name: str) -> Optional[int]:
    """
    Extracts a given port by name from a list of container ports. If
    not port with that name is found then None is returned.

    Args:
        port_list: a list of container ports
        name: the name of the port to extract

    Returns:
        the port with the specified name or None if it doesn't exists
    """
    for port in port_list:
        if port.name == name:
            return port.container_port
    return None


class K8sManager:
    __instance: 'K8sManager' = None
    configuration: Configuration = None
    current_namespace: str = None
    core_v1_api = None

    def __new__(cls):
        if cls.__instance is None:
            try:
                config.load_incluster_config()
            except config.config_exception.ConfigException:
                raise AssertionError("Can't configure Kubernetes client. Not running in a cluster!")

            cls.__instance = super(K8sManager, cls).__new__(cls)
            cls.__instance.configuration = Configuration().values
            cls.__instance.current_namespace = cls.__instance.configuration.kubernetes.namespace
            cls.__instance.core_v1_api = client.CoreV1Api()

            Logger().event(
                category="kubernetes",
                action="kubernetes client configured"
            ).out(severity=Severity.INFO)
        return cls.__instance

    def get_worker_pods(self) -> List[WorkerPod]:
        """
        This function provides the ability to retrieve all of the workers that are
        currently UP in the specified namespace. It uses the Kubernetes API and compiles
        all of the information into a WorkerPod object for ease of use.
        The gathered information is:
            name: the name of the pod in Kubernetes
            ip: the internal ip of the pod from the cluster
            port: the port on witch PID 1 is listening.
                  Usually this port is named "normal" but if the pod doesn't have a port named like that
                  then it assumes that it is using the same port as itself.

        After that the WorkerPod object provides with extra functionality for Pod specific things.

        Returns:
            a list of WorkerPods that are currently up
        """
        assert self.core_v1_api is not None, ""

        worker_selector = self.configuration.kubernetes.worker_selector
        response = self.core_v1_api.list_namespaced_pod(self.current_namespace, label_selector=worker_selector)

        worker_pods = []
        for worker_data in response.items:
            port = get_port_by_name(worker_data.spec.containers[0].ports, "normal")
            port = port or self.configuration.service.port  # We always need some port

            worker_pods.append(WorkerPod(
                name=worker_data.metadata.name,
                ip=worker_data.status.pod_ip,
                port=port
            ))
        return worker_pods

    def get_management_pod(self) -> ManagementPod:
        """
        This function retrieves the ome and only management pod currently up in the
        specified cluster. It gathers all of the needed data into a ManagementPod object.
        The gathered information is:
            name: the name of the pod in Kubernetes
            ip: the internal ip of the pod from the cluster
            port: the port on witch PID 1 is listening.
                  Usually this port is named "normal" but if the pod doesn't have a port named like that
                  then it assumes that it is using the same port as itself.

        Returns:
            a ManagementPod object
        """
        management_selector = self.configuration.kubernetes.management_selector
        response = self.core_v1_api.list_namespaced_pod(self.current_namespace, label_selector=management_selector)

        # Always only one pod is management
        management_data = response.items[0]
        port = get_port_by_name(management_data.spec.containers[0].ports, "normal")
        port = port or self.configuration.service.port  # We always need some port

        return ManagementPod(
            name=management_data.metadata.name,
            ip=management_data.status.pod_ip,
            port=port
        )
