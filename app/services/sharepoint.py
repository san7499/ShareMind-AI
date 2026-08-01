import os

from app.services.graph_api import graph_service
from app.utils.helper import (
    create_directory,
    allowed_document
)
from app.utils.logger import logger
from app.config import DOCUMENT_FOLDER


class SharePointService:

    def __init__(self):
        create_directory(DOCUMENT_FOLDER)

    def list_sites(self):
        """
        Return all SharePoint Sites
        """

        logger.info("Fetching SharePoint Sites...")

        response = graph_service.get_sites()

        return response.get("value", [])

    def list_document_libraries(self, site_id: str):
        """
        Return all document libraries
        """

        logger.info(f"Fetching Libraries for Site {site_id}")

        response = graph_service.get_drives(site_id)

        return response.get("value", [])

    def list_files(self, drive_id: str):
        """
        Return files in root folder
        """

        logger.info(f"Fetching Files from Drive {drive_id}")

        response = graph_service.get_drive_items(drive_id)

        return response.get("value", [])

    def download_document(
        self,
        drive_id: str,
        item_id: str,
        file_name: str
    ):
        """
        Download a single SharePoint document
        """

        destination = os.path.join(
            DOCUMENT_FOLDER,
            file_name
        )

        graph_service.download_file(
            drive_id=drive_id,
            item_id=item_id,
            output_path=destination
        )

        return destination

    def full_sync(self, site_id: str):
        """
        Full Synchronization

        Downloads every supported document from
        every document library.
        """

        logger.info("Starting Full SharePoint Sync")

        synced_documents = []

        libraries = self.list_document_libraries(site_id)

        for library in libraries:

            drive_id = library["id"]

            files = self.list_files(drive_id)

            for file in files:

                if "folder" in file:
                    continue

                file_name = file["name"]

                if not allowed_document(file_name):
                    continue

                logger.info(f"Downloading {file_name}")

                path = self.download_document(
                    drive_id,
                    file["id"],
                    file_name
                )

                synced_documents.append(
                    {
                        "name": file_name,
                        "path": path
                    }
                )

        logger.info(
            f"Synchronization Complete ({len(synced_documents)} files)"
        )

        return synced_documents


sharepoint_service = SharePointService()