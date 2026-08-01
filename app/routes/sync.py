from fastapi import APIRouter

from app.models.request import SyncRequest
from app.models.response import SyncResponse

router = APIRouter(
    prefix="/sync",
    tags=["SharePoint Sync"]
)


@router.post("/", response_model=SyncResponse)
async def sync_documents(request: SyncRequest):

    return SyncResponse(
        status="success",
        message="SharePoint sync completed successfully.",
        documents_synced=0
    )