from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from .database import Base, engine, get_db
from . import models

from services.recovery_agent import RecoveryAgent


# ==================================================
# FastAPI Application
# ==================================================

app = FastAPI(
    title="RecoverAI API",
    description="AI-powered revenue recovery and transaction decision engine",
    version="1.0.0"
)


# ==================================================
# Recovery Agent
# ==================================================

recovery_agent = RecoveryAgent()


# ==================================================
# Request Schema
# ==================================================

class TransactionRequest(BaseModel):

    transaction_id: str = Field(
        ...,
        example="TXN-TEST-001"
    )

    customer_id: str = Field(
        ...,
        example="CUST-1001"
    )

    amount: float = Field(
        ...,
        gt=0,
        example=12500
    )

    failure_reason: str = Field(
        ...,
        example="temporary_bank_decline"
    )

    previous_successes: int = Field(
        ...,
        ge=0,
        example=8
    )

    previous_failures: int = Field(
        ...,
        ge=0,
        example=1
    )

    customer_lifetime_value: float = Field(
        ...,
        ge=0,
        example=75000
    )

    retry_count: int = Field(
        ...,
        ge=0,
        example=1
    )

    days_since_last_payment: int = Field(
        ...,
        ge=0,
        example=5
    )

    checkout_duration: int = Field(
        ...,
        ge=0,
        example=240
    )

    payment_method: str = Field(
        ...,
        example="card"
    )

    risk_score: float = Field(
        ...,
        ge=0,
        le=1,
        example=0.25
    )


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():

    return {
        "message": "RecoverAI backend is running!",
        "version": "1.0.0",
        "status": "operational"
    }


# ==================================================
# Health Check
# ==================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "recoverai-backend"
    }


# ==================================================
# Analyze Transaction
# ==================================================

from .schemas import TransactionRequest


@app.post("/analyze")
def analyze_transaction(transaction: TransactionRequest):

    result = recovery_agent.analyze_transaction(
        transaction.model_dump()
    )

    return result

    try:

        # ------------------------------------------
        # Run Recovery Agent
        # ------------------------------------------

        result = recovery_agent.analyze_transaction(
            transaction.model_dump()
        )

        decision = result.get("decision", {})

        recovery_probability = result.get(
            "recovery_probability",
            0
        )

        action = decision.get(
            "action",
            "manual_review"
        )

        should_execute = decision.get(
            "should_execute",
            False
        )

        reason = decision.get(
            "reason",
            ""
        )

        # ------------------------------------------
        # Check if transaction already exists
        # ------------------------------------------

        existing_case = db.query(
            models.RecoveryCase
        ).filter(
            models.RecoveryCase.case_id
            == transaction.transaction_id
        ).first()

        # ------------------------------------------
        # Create or update database record
        # ------------------------------------------

        if existing_case:

            case = existing_case

        else:

            case = models.RecoveryCase(
                case_id=transaction.transaction_id,
                customer_id=transaction.customer_id,
                payment_id=transaction.transaction_id,
                event_type="PAYMENT_FAILURE",
                amount=transaction.amount,
                failure_reason=transaction.failure_reason,
                previous_successes=transaction.previous_successes,
                previous_failures=transaction.previous_failures,
                customer_lifetime_value=transaction.customer_lifetime_value,
                retry_count=transaction.retry_count,
                risk_score=transaction.risk_score
            )

            db.add(case)

        # ------------------------------------------
        # Store AI analysis
        # ------------------------------------------

        case.recovery_probability = recovery_probability
        case.recommended_action = action
        case.policy_decision = reason

        if should_execute:
            case.action_status = "RECOMMENDED"
        else:
            case.action_status = "PENDING"

        db.commit()
        db.refresh(case)

        # ------------------------------------------
        # Return result
        # ------------------------------------------

        return result

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Transaction analysis failed: {str(e)}"
        )


# ==================================================
# Get All Transactions
# ==================================================

@app.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db)
):

    cases = (
        db.query(models.RecoveryCase)
        .order_by(
            models.RecoveryCase.created_at.desc()
        )
        .all()
    )

    return {
        "total": len(cases),
        "transactions": [
            {
                "case_id": case.case_id,
                "customer_id": case.customer_id,
                "amount": case.amount,
                "failure_reason": case.failure_reason,
                "recovery_probability": case.recovery_probability,
                "recommended_action": case.recommended_action,
                "action_status": case.action_status,
                "risk_score": case.risk_score,
                "created_at": case.created_at
            }
            for case in cases
        ]
    }


# ==================================================
# Get Single Transaction
# ==================================================

@app.get("/transactions/{case_id}")
def get_transaction(
    case_id: str,
    db: Session = Depends(get_db)
):

    case = (
        db.query(models.RecoveryCase)
        .filter(
            models.RecoveryCase.case_id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "case_id": case.case_id,
        "customer_id": case.customer_id,
        "payment_id": case.payment_id,
        "event_type": case.event_type,
        "amount": case.amount,
        "failure_reason": case.failure_reason,
        "previous_successes": case.previous_successes,
        "previous_failures": case.previous_failures,
        "customer_lifetime_value": case.customer_lifetime_value,
        "retry_count": case.retry_count,
        "risk_score": case.risk_score,
        "recovery_probability": case.recovery_probability,
        "recommended_action": case.recommended_action,
        "policy_decision": case.policy_decision,
        "action_status": case.action_status,
        "amount_recovered": case.amount_recovered,
        "created_at": case.created_at,
        "resolved_at": case.resolved_at
    }


# ==================================================
# Recovery Statistics
# ==================================================

@app.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    cases = (
        db.query(models.RecoveryCase)
        .all()
    )

    total_transactions = len(cases)

    total_amount = sum(
        case.amount or 0
        for case in cases
    )

    total_recovered = sum(
        case.amount_recovered or 0
        for case in cases
    )

    average_recovery_probability = (
        sum(
            case.recovery_probability or 0
            for case in cases
        ) / total_transactions
        if total_transactions > 0
        else 0
    )

    high_priority = sum(
        1
        for case in cases
        if (case.recovery_probability or 0) >= 0.70
    )

    recommended_actions = sum(
        1
        for case in cases
        if case.action_status == "RECOMMENDED"
    )

    return {
        "total_transactions": total_transactions,
        "total_transaction_value": round(
            total_amount,
            2
        ),
        "total_amount_recovered": round(
            total_recovered,
            2
        ),
        "average_recovery_probability": round(
            average_recovery_probability,
            4
        ),
        "high_recovery_opportunities": high_priority,
        "recommended_actions": recommended_actions
    }


# ==================================================
# Database Initialization
# ==================================================

Base.metadata.create_all(
    bind=engine
)