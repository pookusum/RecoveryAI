from fastapi import FastAPI

from .database import Base, engine
from . import models

from services.recovery_agent import RecoveryAgent


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="RecoverAI",
    description="AI-powered revenue recovery agent",
    version="0.1.0"
)


# Initialize recovery agent
recovery_agent = RecoveryAgent()


@app.get("/")
def root():
    return {
        "message": "RecoverAI backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "recoverai-backend"
    }


@app.post("/analyze")
def analyze_transaction(transaction: dict):

    result = recovery_agent.analyze_transaction(
        transaction
    )

    return result