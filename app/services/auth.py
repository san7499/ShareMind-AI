from msal import ConfidentialClientApplication
from app.config import (
    TENANT_ID,
    CLIENT_ID,
    CLIENT_SECRET,
)
from app.utils.logger import logger


class AuthService:
    """Handles Microsoft Entra ID authentication."""

    def __init__(self):
        self.authority = f"https://login.microsoftonline.com/{TENANT_ID}"

        self.scopes = [
            "https://graph.microsoft.com/.default"
        ]

        self.app = ConfidentialClientApplication(
            client_id=CLIENT_ID,
            authority=self.authority,
            client_credential=CLIENT_SECRET,
        )

    def get_access_token(self) -> str:
        """
        Acquire an access token for Microsoft Graph API.

        Returns:
            str: Access token

        Raises:
            Exception: If authentication fails.
        """

        logger.info("Requesting Microsoft Graph access token...")

        result = self.app.acquire_token_for_client(
            scopes=self.scopes
        )

        if "access_token" in result:
            logger.info("Access token acquired successfully.")
            return result["access_token"]

        error = result.get("error_description", "Unknown authentication error")

        logger.error(error)

        raise Exception(f"Authentication failed: {error}")


# Singleton instance
auth_service = AuthService()