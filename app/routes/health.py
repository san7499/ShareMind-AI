"""
health.py

Health check endpoints for ShareMind AI.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.response import HealthResponse
from app.utils.logger import logger

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the current health status of the ShareMind AI application."
)
async def health():
    """
    Health Check Endpoint

    Used by monitoring systems to verify that the
    application is running correctly.
    """

    logger.info("Health check requested.")

    response = HealthResponse(
        status="healthy",
        application="ShareMind AI",
        version="1.0.0"
    )

    return JSONResponse(
        status_code=200,
        content=response.model_dump()
    )