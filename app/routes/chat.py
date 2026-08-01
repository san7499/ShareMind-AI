from fastapi import APIRouter

from app.models.request import ChatRequest
from app.models.response import ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    return ChatResponse(
        answer=f"You asked: {request.question}",
        source="Demo",
        confidence=1.0
    )