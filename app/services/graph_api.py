import os
import requests

from app.config import (
    GRAPH_BASE_URL,
    GRAPH_REQUEST_TIMEOUT,
    GRAPH_DOWNLOAD_TIMEOUT,
)
from app.utils.logger import logger

# Check whether auth_service is available (handles missing Microsoft Entra credentials gracefully)
try:
    from app.services.auth import auth_service
except ImportError:
    auth_service = None


class GraphAPIService:
    """
    Microsoft Graph API Client
    """

    def __init__(self):
        self.base_url = GRAPH_BASE_URL

    def _headers(self):
        if auth_service is None or not hasattr(auth_service, "get_access_token"):
            raise RuntimeError("Microsoft Entra ID is not configured.")

        token = auth_service.get_access_token()

        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

    def get(self, endpoint: str):
        """
        Generic GET request
        """
        url = f"{self.base_url}{endpoint}"

        logger.info(f"GET {url}")

        response = requests.get(
            url,
            headers=self._headers(),
            timeout=GRAPH_REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    def get_sites(self):
        """
        Get SharePoint Sites
        """
        return self.get("/sites?search=*")

    def get_drives(self, site_id: str):
        """
        Get Document Libraries
        """
        return self.get(f"/sites/{site_id}/drives")

    def get_drive_items(self, drive_id: str):
        """
        Get Files/Folders
        """
        return self.get(f"/drives/{drive_id}/root/children")

    def get_item_children(self, drive_id: str, item_id: str):
        """
        Get Folder Contents
        """
        return self.get(
            f"/drives/{drive_id}/items/{item_id}/children"
        )

    def download_file(
        self,
        drive_id: str,
        item_id: str,
        output_path: str
    ):
        """
        Download SharePoint File
        """
        endpoint = f"/drives/{drive_id}/items/{item_id}/content"
        url = f"{self.base_url}{endpoint}"

        # Ensure parent directory exists before writing file
        parent_dir = os.path.dirname(os.path.abspath(output_path))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        filename = os.path.basename(output_path)
        logger.info(f"Downloading file '{filename}' (Item ID: {item_id}) from Drive ID: {drive_id}")

        response = requests.get(
            url,
            headers=self._headers(),
            timeout=GRAPH_DOWNLOAD_TIMEOUT,
            stream=True
        )

        response.raise_for_status()

        downloaded_bytes = 0
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_bytes += len(chunk)

        logger.info(f"Successfully saved -> {output_path} ({downloaded_bytes} bytes downloaded)")

        return output_path


graph_service = GraphAPIService()