import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# Microsoft Entra ID
# ===========================
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# ===========================
# SharePoint
# ===========================
SHAREPOINT_SITE_ID = os.getenv("SHAREPOINT_SITE_ID")
SHAREPOINT_DRIVE_ID = os.getenv("SHAREPOINT_DRIVE_ID")

# ===========================
# Microsoft Graph
# ===========================
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

# ===========================
# Ollama
# ===========================
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# ===========================
# ChromaDB
# ===========================
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")

# ===========================
# Documents
# ===========================
DOCUMENT_FOLDER = "./data/documents"