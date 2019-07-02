from datetime import datetime

from kubi_ecs_logger import Logger, Severity
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from redirectory.libs_int.database import DatabaseManager

base = DatabaseManager().get_base()


class RedirectRule(base):
    __tablename__ = "redirect_rule"

    id = Column(Integer, autoincrement=True, primary_key=True)

    domain_rule_id = Column(Integer, ForeignKey('domain_rule.id'), nullable=False)
    domain_rule = relationship("DomainRule", lazy="joined", foreign_keys=[domain_rule_id])

    path_rule_id = Column(Integer, ForeignKey("path_rule.id"), nullable=False)
    path_rule = relationship("PathRule", lazy="joined", foreign_keys=[path_rule_id])

    destination_rule_id = Column(Integer, ForeignKey("destination_rule.id"), nullable=False)
    destination_rule = relationship("DestinationRule", lazy="joined", foreign_keys=[destination_rule_id])

    weight = Column(Integer, nullable=False, default=100)

    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now())

    __table_args__ = (UniqueConstraint('domain_rule_id', 'path_rule_id', 'destination_rule_id',
                                       name='_domain_path_destination_uc'),)

    def modify(self):
        self.modified_at = datetime.now()

    def delete(self, db_session, safe: bool = True):
        db_session.delete(self)
        db_session.commit()

        Logger() \
            .event(category="database", action="redirect rule deleted") \
            .log(original=f"Redirect rule with id: {self.id} has been deleted") \
            .out(severity=Severity.DEBUG)

        self.domain_rule.delete(db_session, safe=safe)
        self.path_rule.delete(db_session, safe=safe)
        self.destination_rule.delete(db_session, safe=safe)
