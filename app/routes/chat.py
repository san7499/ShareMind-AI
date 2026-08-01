from fastapi import APIRouter, HTTPException

from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.services.rag import rag_service
from app.utils.logger import logger

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Chat with ShareMind AI",
    description="Processes a user question using the Permission-Aware RAG pipeline."
)
async def chat(request: ChatRequest):
    """
    Chat endpoint.

    Steps:
    1. Receive user question
    2. Execute RAG pipeline
    3. Return generated answer
    """

    try:
        logger.info(f"Received question: {request.question}")

        result = rag_service.answer(request.question)

        logger.info("Answer generated successfully.")

        return ChatResponse(
            answer=result["answer"],
            source=", ".join(
                source.get("file", "Unknown")
                for source in result.get("sources", [])
            ) if result.get("sources") else "No source found",
            confidence=1.0
        )

    except Exception as error:
        logger.exception("Chat endpoint failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(error)}"
        )