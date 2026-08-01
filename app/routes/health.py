from fastapi import APIRouter

from app.models.response import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/", response_model=HealthResponse)
async def health():

    return HealthResponse(
        status="healthy",
        application="ShareMind AI",
        version="1.0.0"
    )