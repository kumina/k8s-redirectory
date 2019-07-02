from datetime import datetime

from kubi_ecs_logger import Logger, Severity
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, select, func

from redirectory.libs_int.database import DatabaseManager

base = DatabaseManager().get_base()


class DestinationRule(base):
    __tablename__ = "destination_rule"

    id = Column(Integer, autoincrement=True, primary_key=True)
    destination_url = Column(String(1000))
    is_rewrite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now())
    __table_args__ = (UniqueConstraint("destination_url", "is_rewrite", name="_destination_rewrite_uc"),)

    def modify(self):
        self.modified_at = datetime.now()

    def delete(self, db_session, safe: bool = True):
        if safe:
            from redirectory.libs_int.database import get_usage_count
            if get_usage_count(db_session, type(self), self.id) > 0:
                return

        db_session.delete(self)
        db_session.commit()

        Logger() \
            .event(category="database", action="destination deleted") \
            .log(original=f"Destination with id: {self.id} has been deleted") \
            .out(severity=Severity.DEBUG)
