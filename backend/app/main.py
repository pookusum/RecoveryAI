from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from .database import Base, engine, get_db
from . import models
from services.recovery_agent import RecoveryAgent


app = FastAPI(
    title="RecoverAI API",
    description="AI-powered revenue recovery and transaction decision engine",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recovery_agent = RecoveryAgent()

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


@app.get("/")
def root():

    return {
        "message": "RecoverAI backend is running!",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "recoverai-backend"
    }
# Analyze Transaction

@app.post("/analyze")
def analyze_transaction(
    transaction: TransactionRequest,
    db: Session = Depends(get_db)
):

    try:

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
        existing_case = (
            db.query(models.RecoveryCase)
            .filter(
                models.RecoveryCase.case_id
                == transaction.transaction_id
            )
            .first()
        )


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

        case.recovery_probability = recovery_probability
        case.recommended_action = action
        case.policy_decision = reason

        if should_execute:
            case.action_status = "RECOMMENDED"
        else:
            case.action_status = "PENDING"

        db.commit()
        db.refresh(case)

        return result

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Transaction analysis failed: {str(e)}"
        )


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


@app.post("/recover/{case_id}")
def execute_recovery(
    case_id: str,
    db: Session = Depends(get_db)
):

    try:
        # Find recovery case
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
                detail="Recovery case not found"
            )


        if case.action_status != "RECOMMENDED":

            raise HTTPException(
                status_code=400,
                detail="Recovery action is not recommended for this transaction"
            )

        case.amount_recovered = case.amount

        case.action_status = "EXECUTED"

        case.resolved_at = datetime.utcnow()

        
        # Save recovery result

        db.commit()
        db.refresh(case)

        return {
            "success": True,
            "case_id": case.case_id,
            "action": case.recommended_action,
            "status": case.action_status,
            "amount_recovered": case.amount_recovered,
            "message": "Recovery action executed successfully"
        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Recovery execution failed: {str(e)}"
        )

# Recovery Statistics


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

# Database 

Base.metadata.create_all(
    bind=engine
)

# Audit Log

@app.get("/audit-log")
def get_audit_log(
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
        "audit_log": [
            {
                "case_id": case.case_id,
                "customer_id": case.customer_id,
                "amount": case.amount,
                "recovery_probability": case.recovery_probability,
                "recommended_action": case.recommended_action,
                "policy_decision": case.policy_decision,
                "action_status": case.action_status,
                "amount_recovered": case.amount_recovered or 0,
                "created_at": case.created_at,
                "resolved_at": case.resolved_at
            }
            for case in cases
        ]
    }