from datetime import datetime
from typing import Dict, Any
import uuid


def create_audit_record(
    transaction_id: str,
    action: str,
    reason: str,
    recovery_probability: float,
    status: str,
) -> Dict[str, Any]:

    return {
        "audit_id": f"REC-{uuid.uuid4().hex[:8].upper()}",
        "transaction_id": transaction_id,
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "reason": reason,
        "recovery_probability": round(recovery_probability, 4),
        "status": status,
    }   