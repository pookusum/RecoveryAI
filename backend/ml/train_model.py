import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "revenue_recovery_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "recovery_model.joblib"
)


def train_model():

    print("=" * 60)
    print("RecoverAI - Recovery Prediction Model")
    print("=" * 60)

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    print(f"\nDataset loaded: {len(df)} records")

    # Features used before recovery decision
    features = [
        "amount",
        "previous_successes",
        "previous_failures",
        "customer_lifetime_value",
        "retry_count",
        "days_since_last_payment",
        "checkout_duration",
        "payment_method",
        "failure_reason",
        "risk_score"
    ]

    target = "recovered"

    X = df[features]
    y = df[target]

    # Separate numerical and categorical features
    numerical_features = [
        "amount",
        "previous_successes",
        "previous_failures",
        "customer_lifetime_value",
        "retry_count",
        "days_since_last_payment",
        "checkout_duration",
        "risk_score"
    ]

    categorical_features = [
        "payment_method",
        "failure_reason"
    ]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            )
        ],
        remainder="passthrough"
    )

    # Logistic Regression model
    classifier = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    # Complete pipeline
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ]
    )

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")

    # Train
    print("\nTraining model...")

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("=" * 60)
    print(f"Model saved to:")
    print(MODEL_PATH)
    print("=" * 60)


if __name__ == "__main__":
    train_model()