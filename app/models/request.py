from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for chatbot queries.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question"
    )


class SyncRequest(BaseModel):
    """
    Request model for SharePoint synchronization.
    """

    site_name: str | None = Field(
        default=None,
        description="Optional SharePoint site name"
    )

    library_name: str | None = Field(
        default=None,
        description="Optional document library name"
    )

    full_sync: bool = Field(
        default=True,
        description="True = Full Sync, False = Incremental Sync"
    )