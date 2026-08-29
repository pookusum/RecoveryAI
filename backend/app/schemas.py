from pydantic import BaseModel, Field
from typing import Optional


class TransactionRequest(BaseModel):

    transaction_id: str
    customer_id: str

    amount: float = Field(gt=0)

    failure_reason: Optional[str] = None

    previous_successes: int = Field(default=0, ge=0)
    previous_failures: int = Field(default=0, ge=0)

    customer_lifetime_value: float = Field(default=0, ge=0)

    retry_count: int = Field(default=0, ge=0)

    days_since_last_payment: int = Field(default=0, ge=0)

    checkout_duration: int = Field(default=0, ge=0)

    payment_method: Optional[str] = None

    risk_score: float = Field(default=0, ge=0, le=1)


class ExecuteRequest(BaseModel):
    action: str