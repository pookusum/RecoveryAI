from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from .database import Base


class RecoveryCase(Base):
    __tablename__ = "recovery_cases"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(String, unique=True, index=True, nullable=False)

    customer_id = Column(String, index=True, nullable=False)
    payment_id = Column(String, index=True, nullable=True)

    event_type = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    failure_reason = Column(String, nullable=True)

    previous_successes = Column(Integer, default=0)
    previous_failures = Column(Integer, default=0)

    customer_lifetime_value = Column(Float, default=0)

    retry_count = Column(Integer, default=0)

    risk_score = Column(Float, default=0)

    recovery_probability = Column(Float, nullable=True)

    recommended_action = Column(String, nullable=True)

    policy_decision = Column(String, nullable=True)

    action_status = Column(String, default="PENDING")

    amount_recovered = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)