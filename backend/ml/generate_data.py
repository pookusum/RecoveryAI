import os
import numpy as np
import pandas as pd


np.random.seed(42)

NUM_RECORDS = 5000


def generate_dataset():
    data = []

    failure_reasons = [
        "temporary_bank_decline",
        "insufficient_balance",
        "network_error",
        "authentication_failure",
        "expired_card",
    ]

    payment_methods = [
        "card",
        "upi",
        "netbanking",
        "wallet",
    ]

    for i in range(NUM_RECORDS):

        amount = round(np.random.uniform(200, 50000), 2)

        previous_successes = np.random.poisson(8)

        previous_failures = np.random.poisson(1.5)

        customer_lifetime_value = round(
            np.random.uniform(1000, 200000), 2
        )

        retry_count = np.random.randint(0, 5)

        days_since_last_payment = np.random.randint(1, 180)

        checkout_duration = np.random.randint(5, 600)

        failure_reason = np.random.choice(
            failure_reasons,
            p=[0.30, 0.20, 0.15, 0.15, 0.20]
        )

        payment_method = np.random.choice(
            payment_methods,
            p=[0.35, 0.40, 0.15, 0.10]
        )

        # Customer/payment risk score.
        # Higher value means higher risk.
        risk_score = (
            0.30 * min(previous_failures / 10, 1)
            + 0.25 * min(retry_count / 5, 1)
            + 0.20 * min(amount / 50000, 1)
            + 0.15 * min(days_since_last_payment / 180, 1)
            + np.random.normal(0, 0.05)
        )

        risk_score = float(np.clip(risk_score, 0, 1))

        # Base recovery score.
        recovery_score = 0.45

        # Strong payment history improves recovery chances.
        recovery_score += min(previous_successes * 0.025, 0.25)

        # Previous failures reduce recovery chances.
        recovery_score -= min(previous_failures * 0.035, 0.25)

        # Repeated retries reduce recovery chances.
        recovery_score -= retry_count * 0.08

        # High risk reduces recovery chances.
        recovery_score -= risk_score * 0.30

        # Failure reason matters.
        if failure_reason == "temporary_bank_decline":
            recovery_score += 0.15

        elif failure_reason == "network_error":
            recovery_score += 0.10

        elif failure_reason == "insufficient_balance":
            recovery_score -= 0.08

        elif failure_reason == "expired_card":
            recovery_score -= 0.12

        elif failure_reason == "authentication_failure":
            recovery_score -= 0.05

        # Very recent customer activity is a positive signal.
        if days_since_last_payment <= 14:
            recovery_score += 0.08

        # Long checkout sessions can indicate stronger intent.
        if checkout_duration >= 120:
            recovery_score += 0.05

        # Add some randomness so the model doesn't get a perfect answer.
        recovery_score += np.random.normal(0, 0.10)

        recovery_probability = float(
            np.clip(recovery_score, 0.02, 0.98)
        )

        # Actual outcome.
        recovered = np.random.binomial(
            1,
            recovery_probability
        )

        data.append({
            "transaction_id": f"TXN-{i + 1:05d}",
            "customer_id": f"CUST-{np.random.randint(1000, 9999)}",
            "amount": amount,
            "failure_reason": failure_reason,
            "previous_successes": previous_successes,
            "previous_failures": previous_failures,
            "customer_lifetime_value": customer_lifetime_value,
            "retry_count": retry_count,
            "days_since_last_payment": days_since_last_payment,
            "checkout_duration": checkout_duration,
            "payment_method": payment_method,
            "risk_score": round(risk_score, 3),
            "recovered": recovered,
        })

    return pd.DataFrame(data)


if __name__ == "__main__":

    df = generate_dataset()

    data_directory = os.path.join(
        os.path.dirname(__file__),
        "data"
    )

    os.makedirs(data_directory, exist_ok=True)

    output_path = os.path.join(
        data_directory,
        "revenue_recovery_data.csv"
    )

    df.to_csv(output_path, index=False)

    print("=" * 50)
    print("RecoverAI dataset generated successfully")
    print("=" * 50)
    print(f"Records: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {output_path}")
    print()
    print("Recovery distribution:")
    print(df["recovered"].value_counts())
    print()
    print("First 5 records:")
    print(df.head())