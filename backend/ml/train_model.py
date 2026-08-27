import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
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


FEATURES = [
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

TARGET = "recovered"


NUMERICAL_FEATURES = [
    "amount",
    "previous_successes",
    "previous_failures",
    "customer_lifetime_value",
    "retry_count",
    "days_since_last_payment",
    "checkout_duration",
    "risk_score"
]

CATEGORICAL_FEATURES = [
    "payment_method",
    "failure_reason"
]


def build_preprocessor():

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES
            )
        ],
        remainder="passthrough"
    )


def evaluate_model(name, model, X_test, y_test):

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities)
    }

    print("\n" + "-" * 55)
    print(name)
    print("-" * 55)

    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1']:.4f}")
    print(f"ROC-AUC:   {metrics['roc_auc']:.4f}")

    return metrics


def train_model():

    print("=" * 60)
    print("RecoverAI - Model Training")
    print("=" * 60)

    # Load data
    df = pd.read_csv(DATA_PATH)

    print(f"\nDataset loaded: {len(df)} records")

    X = df[FEATURES]
    y = df[TARGET]

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

    # -------------------------------------------------
    # Model 1: Logistic Regression (baseline)
    # -------------------------------------------------

    logistic_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor()
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced"
                )
            )
        ]
    )

    print("\nTraining Logistic Regression...")
    logistic_pipeline.fit(X_train, y_train)

    logistic_metrics = evaluate_model(
        "LOGISTIC REGRESSION - BASELINE",
        logistic_pipeline,
        X_test,
        y_test
    )

    # -------------------------------------------------
    # Model 2: Random Forest
    # -------------------------------------------------

    random_forest_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor()
            ),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    min_samples_leaf=5,
                    max_features="sqrt",
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )

    print("\nTraining Random Forest...")
    random_forest_pipeline.fit(X_train, y_train)

    random_forest_metrics = evaluate_model(
        "RANDOM FOREST",
        random_forest_pipeline,
        X_test,
        y_test
    )

    # -------------------------------------------------
    # Select model using ROC-AUC
    # -------------------------------------------------

    if random_forest_metrics["roc_auc"] > logistic_metrics["roc_auc"]:
        best_model = random_forest_pipeline
        best_name = "Random Forest"
        best_metrics = random_forest_metrics
    else:
        best_model = logistic_pipeline
        best_name = "Logistic Regression"
        best_metrics = logistic_metrics

    print("\n" + "=" * 60)
    print("MODEL SELECTION")
    print("=" * 60)

    print(f"Selected model: {best_name}")
    print(f"ROC-AUC: {best_metrics['roc_auc']:.4f}")
    print(f"F1 Score: {best_metrics['f1']:.4f}")

    # Save selected model
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(best_model, MODEL_PATH)

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\n" + "=" * 60)
    print("RecoverAI model training complete")
    print("=" * 60)


if __name__ == "__main__":
    train_model()