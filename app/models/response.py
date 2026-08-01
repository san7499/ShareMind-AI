from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    Response returned by chatbot.
    """

    answer: str
    source: str
    confidence: float


class SyncResponse(BaseModel):
    """
    Response returned after SharePoint synchronization.
    """

    status: str
    message: str
    documents_synced: int


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    application: str
    version: str