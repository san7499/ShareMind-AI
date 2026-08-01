import requests

from app.config import GRAPH_BASE_URL
from app.services.auth import auth_service
from app.utils.logger import logger


class GraphAPIService:
    """
    Microsoft Graph API Client
    """

    def __init__(self):
        self.base_url = GRAPH_BASE_URL

    def _headers(self):
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
            timeout=60
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

        endpoint = (
            f"/drives/{drive_id}/items/{item_id}/content"
        )

        url = f"{self.base_url}{endpoint}"

        logger.info(f"Downloading {item_id}")

        response = requests.get(
            url,
            headers=self._headers(),
            timeout=120,
            stream=True
        )

        response.raise_for_status()

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(8192):
                if chunk:
                    file.write(chunk)

        logger.info(f"Saved -> {output_path}")

        return output_path


graph_service = GraphAPIService()