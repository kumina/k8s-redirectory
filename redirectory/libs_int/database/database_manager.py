import os
import threading
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from kubi_ecs_logger import Logger, Severity

from redirectory.libs_int.config.configuration import Configuration


def get_current_thread_id() -> Optional[int]:
    """
    Returns the ID of the thread where the function was called
    """
    return threading.current_thread().ident


def get_connection_string():
    """
    Generates a connection string to be passed to SQLAlchemy.
    The string is created from the current loaded configuration with
    the help of the Configuration() class.
    There are two options for both SQLite and MySQL database connections.

    Returns:
        a connection string for SQLAlchemy to use for an engine
    """
    config = Configuration().values
    db = config.database
    db_path = os.path.join(config.directories.data, db.path)

    if config.deployment == 'test':
        return 'sqlite://'

    if db.type == "sqlite":
        return f"sqlite:///{db_path}"
    else:
        return f"{db.type}://{db.username}:{db.password}@{db.host}:{db.port}/{db.name}"


class DatabaseManager:
    __instance: Optional['DatabaseManager'] = None
    __engine = None
    __initialized: bool = False
    __base = None

    __sessions: dict = {}
    __session_maker = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DatabaseManager, cls).__new__(cls)

            connection_string = get_connection_string()
            cls.__instance.__engine = create_engine(connection_string, echo=False)
            cls.__instance.__base = declarative_base(bind=cls.__instance.__engine)

            cls.__instance.__session_maker = sessionmaker(expire_on_commit=True, autoflush=True)
            cls.__instance.__sessions = {}
            cls.__initialized = True

            Logger().event(
                category="database",
                action="database loaded",
                dataset=connection_string
            ).out(severity=Severity.INFO)

        return cls.__instance

    def reload(self):
        self.__instance = None
        # TODO:
        pass

    def get_session(self):
        """
        Creates a scoped session with with the help of the session maker.
        This session is specific to the current thread from where this function is called.
        If a session already exists it will be returned but if not a new one will be created.
        If the DatabaseManager is not initialized then a ValueError will be raised.

        Returns:
            a database session for the current thread
        """
        if self.__initialized:
            # Get thread id
            thread_id = get_current_thread_id()

            # Check if we already have a session for this thread
            if thread_id in self.__sessions.keys():
                if self.__sessions[thread_id] is None:
                    self.__sessions[thread_id] = scoped_session(self.__session_maker)
            else:
                self.__sessions[thread_id] = scoped_session(self.__session_maker)

            return self.__sessions[thread_id]
        else:
            raise ValueError("DatabaseManager must be initialized!")

    def return_session(self, session):
        """
        Closes the given session and removes it from DatabaseManager to prevent from any further use.
        The function will call remove() on the passed in session and will null out the session in the
        self.__sessions dict corresponding to the thread id the function is getting called in.
        Sets the session of the DatabaseManager to None

        Args:
            session: the session to remove
        """
        session.remove()
        # Get thread id
        thread_id = get_current_thread_id()
        if thread_id in self.__sessions:
            self.__sessions[thread_id] = None

    def get_base(self):
        """
        Gets the current base that all models should inherit from.
        Once a model inherits from this base it will be associated with it.

        Returns:
            the current base
        """
        if self.__initialized:
            return self.__base
        else:
            raise ValueError("DatabaseManager must be initialized!")

    def delete_db_tables(self):
        """
        Will drop all tables associated with the current base of the DatabaseManager.
        Every model's table that inherits from this base will be dropped.
        If the DatabaseManager is not initialized then a ValueError will be raised.
        """
        if self.__initialized:
            self.__base.metadata.drop_all()
        else:
            raise ValueError("DatabaseManager must be initialized!")

    def create_db_tables(self):
        """
        Will create all model's tables associated with the current DatabaseManager base.
        The creation of those tables is safe. If a table already exists it will not be created again.
        If the DatabaseManager is not initialized then a ValueError will be raised.
        """
        if self.__initialized:
            self.__base.metadata.create_all(checkfirst=True)
        else:
            raise ValueError("DatabaseManager must be initialized!")
