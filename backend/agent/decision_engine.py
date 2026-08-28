from typing import Dict, Any


class RecoveryDecisionEngine:

    def decide(
        self,
        recovery_probability: float,
        failure_reason: str,
        retry_count: int,
        amount: float,
        risk_score: float,
    ) -> Dict[str, Any]:

        probability = recovery_probability

        # -------------------------------------------------
        # SAFETY / STOPPING RULE
        # -------------------------------------------------

        if retry_count >= 3:
            return {
                "action": "escalate",
                "priority": "high",
                "reason": (
                    "Automatic recovery stopped because the "
                    "maximum retry threshold has been reached."
                ),
                "should_execute": False,
            }

        # -------------------------------------------------
        # HIGH RECOVERY PROBABILITY
        # -------------------------------------------------

        if probability >= 0.70:

            if failure_reason in [
                "temporary_bank_decline",
                "network_error",
            ]:
                return {
                    "action": "smart_retry",
                    "priority": "high",
                    "reason": (
                        "The transaction has a high recovery probability "
                        "and the failure appears temporary."
                    ),
                    "should_execute": True,
                }

            if failure_reason == "authentication_failure":
                return {
                    "action": "recovery_link",
                    "priority": "medium",
                    "reason": (
                        "The transaction has good recovery potential, "
                        "but authentication issues should be resolved "
                        "before retrying."
                    ),
                    "should_execute": True,
                }

            return {
                "action": "recovery_link",
                "priority": "medium",
                "reason": (
                    "The transaction has a high probability of recovery. "
                    "A recovery link is safer than repeated automatic retries."
                ),
                "should_execute": True,
            }

        # -------------------------------------------------
        # MEDIUM RECOVERY PROBABILITY
        # -------------------------------------------------

        if probability >= 0.40:

            if failure_reason == "insufficient_balance":
                return {
                    "action": "payment_reminder",
                    "priority": "medium",
                    "reason": (
                        "Recovery is possible, but insufficient balance "
                        "makes an immediate retry less suitable."
                    ),
                    "should_execute": True,
                }

            return {
                "action": "recovery_link",
                "priority": "medium",
                "reason": (
                    "The transaction has moderate recovery potential. "
                    "A recovery link provides a bounded intervention."
                ),
                "should_execute": True,
            }

        # -------------------------------------------------
        # LOW RECOVERY PROBABILITY
        # -------------------------------------------------

        if amount >= 25000 or risk_score >= 0.70:
            return {
                "action": "escalate",
                "priority": "high",
                "reason": (
                    "Recovery probability is low and the transaction "
                    "has significant financial or risk exposure."
                ),
                "should_execute": False,
            }

        return {
            "action": "payment_reminder",
            "priority": "low",
            "reason": (
                "Recovery probability is low, so aggressive automated "
                "retries are avoided."
            ),
            "should_execute": True,
        }