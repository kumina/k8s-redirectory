import os
import io
import zipfile
from typing import List, Optional

from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.config import Configuration
from redirectory.libs_int.database import DatabaseManager
from redirectory.libs_int.hyperscan import get_hs_db_version, HsManager
from redirectory.libs_int.kubernetes import K8sManager, WorkerPod, ManagementPod
from redirectory.libs_int.metrics import HYPERSCAN_DB_COMPILED_TOTAL, HYPERSCAN_DB_VERSION, HYPERSCAN_DB_RELOADED_TOTAL


class Synchronizer:
    __instance: 'Synchronizer' = None
    configuration: Configuration = None
    current_hs_db_version: str = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Synchronizer, cls).__new__(cls)
            cls.__instance.configuration = Configuration().values

            # Load current db version from SQL
            _, current_version = get_hs_db_version()
            cls.__instance.current_hs_db_version = current_version

            Logger().event(
                category="synchronizer",
                action="synchronizer configured",
                dataset=f"current hs db version: {current_version}"
            ).out(severity=Severity.INFO)
        return cls.__instance

    @staticmethod
    def management_get_sync_files() -> zipfile.ZipFile:
        """
        Function used to get the zip file with the databases from the management pod

        Returns:
            the databases zipped
        """
        management_pod: ManagementPod = K8sManager().get_management_pod()
        return management_pod.get_sync_zip_file()

    @staticmethod
    def management_update_workers(workers: List[WorkerPod]) -> Optional[List[WorkerPod]]:
        """
        Makes an reload_hs_db request to all of the worker pods given in the list.
        If a reload_hs_db request fails that worker will be added to the failed workers

        Args:
            workers: a list of all the worker pods to update

        Returns:
            list containing all the failed worker pods
        """
        failed_workers = []
        for worker in workers:
            if Synchronizer.management_update_worker(worker) is False:
                failed_workers += worker
        return None if not failed_workers else failed_workers

    @staticmethod
    def management_update_worker(worker: WorkerPod) -> bool:
        """
        Sync the specified worker with the management pod.

        Args:
            worker: the worker pod to update

        Returns:
            if the worker pod started updating itself
        """
        return worker.sync()

    def worker_sync_files(self):
        """
        This function gets called when the application is in worker mode.
        Stops the readiness checks from succeeding.
        Downloads and reloads the databases.
        After that it logs a couple of metrics and also logging.
        """
        Logger() \
            .event(category="synchronizer", action="synchronizer sync started") \
            .out(severity=Severity.INFO)

        db_manager = DatabaseManager()
        hs_manager = HsManager()

        # Mark hs database as not loaded which causes ready check to fail
        hs_manager.database.is_loaded = False

        # Download sync files and write to disc
        sync_zip_file = self.management_get_sync_files()
        self.util_save_sync_zip_file(sync_zip_file)

        # Reload sql
        db_manager.reload()

        # Reload hs
        hs_manager.database.reload_database()
        new_hs_db_version = hs_manager.database.db_version

        # Metrics
        HYPERSCAN_DB_RELOADED_TOTAL.labels(self.configuration.node_type).inc()
        HYPERSCAN_DB_VERSION.labels(self.configuration.node_type).set(new_hs_db_version)

        # Log
        Logger() \
            .event(category="synchronizer", action="synchronizer sync complete",
                   dataset=f"New hs db version: {new_hs_db_version}") \
            .out(severity=Severity.INFO)

    def util_new_hs_db_version_callback(self, new_version: str):
        """
        This function is passed as an event callback function to the CompilerJob.
        When the CompilerJob is done with compiling and saving the Hyperscan databases
        if specified it can call this function.

        The function updates some prometheus metrics and updates both the management pod
        and the worker pods.

        Args:
            new_version: the new version of the just compiled db
        """
        if new_version is self.current_hs_db_version:
            return

        self.current_hs_db_version = new_version

        Logger().event(
            category="synchronizer",
            action="synchronizer new hs db version",
            dataset=f"new hs db version: {new_version}"
        ).out(severity=Severity.INFO)

        # Metrics
        HYPERSCAN_DB_COMPILED_TOTAL.labels(self.configuration.node_type).inc()
        HYPERSCAN_DB_VERSION.labels(self.configuration.node_type).set(new_version)

        # Trigger worker updates
        workers = K8sManager().get_worker_pods()
        if workers:
            Logger().event(
                category="synchronizer",
                action="synchronizer worker updates",
                dataset=f"triggered worker updates for new hs db version: {new_version}"
            ).out(severity=Severity.INFO)
            self.management_update_workers(workers)

        # Trigger management update
        management = K8sManager().get_management_pod()
        if management and management.reload_hs_db():
            Logger().event(
                category="synchronizer",
                action="synchronizer management update",
                dataset=f"triggered management update for new hs db version: {new_version}"
            ).out(severity=Severity.INFO)

    def util_get_sync_files_as_zip(self):
        """
        Gathers the needed files to sync a worker into one in-memory zip file.

        Returns:
            in-memory zip file in a BytesIO object
        """
        data_dir = self.configuration.directories.data
        permitted_files = [
            self.configuration.hyperscan.domain_db,
            self.configuration.hyperscan.rules_db,
            self.configuration.database.path
        ]

        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for file in permitted_files:
                zf.write(os.path.join(data_dir, file), file)
        memory_file.seek(0)
        return memory_file

    def util_save_sync_zip_file(self, sync_zip_file: zipfile.ZipFile):
        """
        Extracts all files of a zip file into the data dir specified in the
        documentation.

        Args:
            sync_zip_file: zip file object to extract
        """
        data_dir = self.configuration.directories.data
        sync_zip_file.extractall(path=data_dir)
