import os
import io
import hyperscan as hs
from typing import List

from kubi_ecs_logger import Logger, Severity

from .hs_actions import get_hs_db_version
from redirectory.libs_int.config import Configuration

HYPERSCAN_DB_MODE = hs.HS_MODE_BLOCK


class HsDatabase:
    domain_db_path: str = None
    rules_db_path: str = None

    domain_db: hs.Database = None
    rules_db: hs.Database = None

    db_version: str = None
    is_loaded: bool = False

    def __init__(self):
        config = Configuration().values

        self.domain_db_path = os.path.join(config.directories.data, config.hyperscan.domain_db)
        self.rules_db_path = os.path.join(config.directories.data, config.hyperscan.rules_db)

    def compile_rules_db(self, expressions: List[bytes], ids: List[int]):
        self.rules_db = HsDatabase.compile_db_in_memory(expressions, ids)

    def compile_domain_db(self, expressions: List[bytes], ids: List[int]):
        self.domain_db = HsDatabase.compile_db_in_memory(expressions, ids)

    def load_database(self):
        """
        TODO:
        """
        self.domain_db = self._load_hs_db(self.domain_db_path)
        self.rules_db = self._load_hs_db(self.rules_db_path)

        if self.domain_db is None or self.rules_db is None:
            self.is_loaded = False
            return

        _, new_db_version = get_hs_db_version()
        self.db_version = new_db_version
        self.is_loaded = True

    def save_database(self):
        self._save_hs_db(self.domain_db_path, self.domain_db)
        self._save_hs_db(self.rules_db_path, self.rules_db)

    def reload_database(self):
        self.load_database()

    @staticmethod
    def compile_db_in_memory(expressions: List[bytes], ids: List[int]) -> hs.Database:
        assert len(expressions) == len(ids), "There must be an id for every expression."

        flags = [hs.HS_FLAG_SOM_LEFTMOST] * len(expressions)
        db = hs.Database(mode=HYPERSCAN_DB_MODE)
        db.compile(expressions=expressions, ids=ids, flags=flags)
        return db

    @staticmethod
    def _load_hs_db(path: str):
        if os.path.isfile(path) is False:
            Logger() \
                .error(message=f"File at path: {path} does not exists") \
                .out(severity=Severity.ERROR)
            return None

        with io.open(path, "rb") as bin_file:
            bin_data = bin_file.read()

        Logger() \
            .event(category="hyperscan", action="hyperscan database loaded", dataset=path) \
            .out(severity=Severity.INFO)
        return hs.loads(bytearray(bin_data))

    @staticmethod
    def _save_hs_db(path: str, db_to_save: hs.Database):
        """
        TODO:
        Args:
            path:
            db_to_save:
        """
        assert db_to_save is not None, "Hyperscan database must not be none in order to save to file"

        serialized_db = hs.dumps(db_to_save)
        with io.open(path, "wb") as bin_file:
            bin_file.write(serialized_db)

        Logger().event(
            category="hyperscan",
            action="hyperscan database saved",
            dataset=path
        ).out(severity=Severity.INFO)
