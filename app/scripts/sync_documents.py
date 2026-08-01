# scripts/sync_documents.py
import sys
from pathlib import Path
from typing import Dict, Any

# Ensure project root is in Python path for direct CLI execution
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.config import SHAREPOINT_SITE_ID, DOCUMENT_FOLDER
from app.services.sharepoint import sharepoint_service
from app.utils.logger import logger


def run_sync() -> Dict[str, Any]:
    """
    Executes SharePoint document synchronization using the configured site ID.
    Returns a dictionary summarizing the operation results.
    """
    logger.info("==========================================")
    logger.info("Starting SharePoint Document Synchronization")
    logger.info("==========================================")

    # 1. Validate required configuration
    if not SHAREPOINT_SITE_ID:
        logger.error("Configuration error: SHAREPOINT_SITE_ID is not set.")
        return {
            "status": "failed",
            "documents_synced": 0,
            "error": "SHAREPOINT_SITE_ID configuration missing"
        }

    try:
        # 2. Call full_sync on exported sharepoint_service singleton
        logger.info(f"Target document folder: '{DOCUMENT_FOLDER}'")
        logger.info(f"Connecting to SharePoint site ID: '{SHAREPOINT_SITE_ID}'...")
        
        downloaded_docs = sharepoint_service.full_sync(site_id=SHAREPOINT_SITE_ID)
        synced_count = len(downloaded_docs) if downloaded_docs else 0

        logger.info("------------------------------------------")
        logger.info(f"Synchronization Completed. Total files: {synced_count}")
        logger.info("------------------------------------------")

        return {
            "status": "success",
            "documents_synced": synced_count
        }

    except Exception as e:
        logger.exception("Synchronization failed due to an unhandled exception.")
        return {
            "status": "failed",
            "documents_synced": 0,
            "error": str(e)
        }


def main():
    """
    Main entry point for CLI execution.
    Prints user-friendly stdout output and exits with code 0 (success) or 1 (failure).
    """
    result = run_sync()

    if result["status"] == "success":
        count = result["documents_synced"]
        print("\nSynchronization completed successfully.")
        print(f"Downloaded {count} document{'s' if count != 1 else ''}.\n")
        sys.exit(0)
    else:
        error_msg = result.get("error", "Unknown error")
        print("\nSynchronization failed!")
        print(f"Error: {error_msg}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()