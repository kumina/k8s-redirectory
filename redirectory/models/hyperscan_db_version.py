from sqlalchemy import Column, Integer, String

from redirectory.libs_int.database import DatabaseManager

base = DatabaseManager().get_base()


class HsDbVersion(base):
    __tablename__ = "hs_db_version"

    id = Column(Integer, autoincrement=True, primary_key=True)
    old_version = Column(String, nullable=True)
    current_version = Column(String, nullable=False)
