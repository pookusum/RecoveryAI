from fastapi import FastAPI

from .database import Base, engine
from . import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="RecoverAI",
    description="AI-powered revenue recovery agent",
    version="0.1.0"
)


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