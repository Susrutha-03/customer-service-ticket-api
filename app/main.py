
import logging
import time

from fastapi import FastAPI, Request
from app.database import engine, Base
from app.routes import tickets
from app import models
from app.logging_config import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Service Ticket API",
    description="An API to manage customer support tickets",
    version="1.0.0"
)

app.include_router(tickets.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = round(time.time() - start_time, 3)

        logger.info(
            "%s %s - Status: %s - Duration: %ss",
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response

    except Exception:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path
        )
        raise

@app.get("/")
def home():
    return {
        "message": "Welcome to Customer Service Ticket API!",
        "status": "Running successfully"
    }