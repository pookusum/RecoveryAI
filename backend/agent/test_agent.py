from decision_engine import RecoveryDecisionEngine


engine = RecoveryDecisionEngine()


test_cases = [
    {
        "name": "Temporary bank decline",
        "probability": 0.82,
        "failure_reason": "temporary_bank_decline",
        "retry_count": 0,
        "amount": 8500,
        "risk_score": 0.21,
    },
    {
        "name": "Insufficient balance",
        "probability": 0.55,
        "failure_reason": "insufficient_balance",
        "retry_count": 1,
        "amount": 12000,
        "risk_score": 0.45,
    },
    {
        "name": "High risk transaction",
        "probability": 0.22,
        "failure_reason": "insufficient_balance",
        "retry_count": 1,
        "amount": 42000,
        "risk_score": 0.82,
    },
    {
        "name": "Retry limit reached",
        "probability": 0.90,
        "failure_reason": "temporary_bank_decline",
        "retry_count": 3,
        "amount": 8000,
        "risk_score": 0.20,
    },
]


for case in test_cases:

    result = engine.decide(
        recovery_probability=case["probability"],
        failure_reason=case["failure_reason"],
        retry_count=case["retry_count"],
        amount=case["amount"],
        risk_score=case["risk_score"],
    )

    print("=" * 60)
    print(case["name"])
    print("Action:", result["action"])
    print("Priority:", result["priority"])
    print("Reason:", result["reason"])
    print("Execute:", result["should_execute"])