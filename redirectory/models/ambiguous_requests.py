from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String

from redirectory.libs_int.database import DatabaseManager

base = DatabaseManager().get_base()


class AmbiguousRequest(base):
    __tablename__ = "ambiguous_request"

    id = Column(Integer, autoincrement=True, primary_key=True)
    request = Column(String(1000), unique=True)
    created_at = Column(DateTime, default=datetime.now())
