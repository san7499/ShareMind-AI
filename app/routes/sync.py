"""
sync.py

SharePoint Synchronization API
"""

from fastapi import APIRouter, HTTPException

from app.models.request import SyncRequest
from app.models.response import SyncResponse
from app.services.sharepoint import sharepoint_service
from app.utils.logger import logger


router = APIRouter(
    prefix="/sync",
    tags=["SharePoint Sync"]
)


@router.post(
    "/",
    response_model=SyncResponse,
    summary="Synchronize SharePoint Documents",
    description="Downloads documents from SharePoint and stores them locally."
)
async def sync_documents(request: SyncRequest):
    """
    Synchronize SharePoint documents.

    Supports:
    - Full synchronization
    - Incremental synchronization (placeholder)
    """

    try:
        logger.info("SharePoint synchronization requested.")

        if request.full_sync:

            documents = sharepoint_service.full_sync(
                site_id=request.site_name
            )

            synced_count = len(documents)

            message = (
                "Full SharePoint synchronization completed successfully."
            )

        else:
            # Placeholder for incremental synchronization
            synced_count = 0

            message = (
                "Incremental synchronization is not implemented yet."
            )

        logger.info(
            f"Synchronization completed. Documents synced: {synced_count}"
        )

        return SyncResponse(
            status="success",
            message=message,
            documents_synced=synced_count
        )

    except Exception as error:

        logger.exception("SharePoint synchronization failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Synchronization failed: {str(error)}"
        )