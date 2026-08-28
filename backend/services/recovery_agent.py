import os
import joblib
import pandas as pd

from agent.decision_engine import RecoveryDecisionEngine
from agent.audit import create_audit_record


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "model",
    "recovery_model.joblib"
)


class RecoveryAgent:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.decision_engine = RecoveryDecisionEngine()

    def analyze_transaction(self, transaction):

        # Features used by the ML model
        features = pd.DataFrame([{
            "amount": transaction["amount"],
            "failure_reason": transaction["failure_reason"],
            "previous_successes": transaction["previous_successes"],
            "previous_failures": transaction["previous_failures"],
            "customer_lifetime_value": transaction[
                "customer_lifetime_value"
            ],
            "retry_count": transaction["retry_count"],
            "days_since_last_payment": transaction[
                "days_since_last_payment"
            ],
            "checkout_duration": transaction[
                "checkout_duration"
            ],
            "payment_method": transaction["payment_method"],
            "risk_score": transaction["risk_score"],
        }])

        # ML prediction
        recovery_probability = float(
            self.model.predict_proba(features)[0][1]
        )

        # Decision engine
        decision = self.decision_engine.decide(
            recovery_probability=recovery_probability,
            failure_reason=transaction["failure_reason"],
            retry_count=transaction["retry_count"],
            amount=transaction["amount"],
            risk_score=transaction["risk_score"],
        )

        # Audit record
        audit = create_audit_record(
            transaction_id=transaction["transaction_id"],
            action=decision["action"],
            reason=decision["reason"],
            recovery_probability=recovery_probability,
            status="recommended",
        )

        return {
            "transaction_id": transaction["transaction_id"],
            "recovery_probability": round(
                recovery_probability,
                4
            ),
            "decision": decision,
            "audit": audit,
        }