"""
config.py

Application Configuration
Loads environment variables from the .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =====================================================
# Microsoft Entra ID
# =====================================================
TENANT_ID = os.getenv("TENANT_ID", "")
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

# =====================================================
# SharePoint
# =====================================================
SHAREPOINT_SITE_ID = os.getenv("SHAREPOINT_SITE_ID", "")
SHAREPOINT_DRIVE_ID = os.getenv("SHAREPOINT_DRIVE_ID", "")

# =====================================================
# Microsoft Graph API
# =====================================================

GRAPH_BASE_URL = os.getenv(
    "GRAPH_BASE_URL",
    "https://graph.microsoft.com/v1.0"
)

GRAPH_REQUEST_TIMEOUT = int(
    os.getenv("GRAPH_REQUEST_TIMEOUT", "60")
)

GRAPH_DOWNLOAD_TIMEOUT = int(
    os.getenv("GRAPH_DOWNLOAD_TIMEOUT", "120")
)

# =====================================================
# Ollama Configuration
# =====================================================
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

# Alias used by llm.py and rag.py
OLLAMA_BASE_URL = OLLAMA_URL

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)

# =====================================================
# Embedding Model
# =====================================================
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# ChromaDB
# =====================================================
CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "./data/chroma_db"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "rag_documents"
)

# =====================================================
# Documents
# =====================================================
DOCUMENT_FOLDER = os.getenv(
    "DOCUMENT_FOLDER",
    "./data/documents"
)

# Alias used by sync_documents.py
DOCUMENTS_DIR = DOCUMENT_FOLDER

# =====================================================
# Chunking
# =====================================================
CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "500")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", "100")
)

# =====================================================
# Retrieval
# =====================================================
TOP_K_RESULTS = int(
    os.getenv("TOP_K_RESULTS", "5")
)

# =====================================================
# Application
# =====================================================
APP_NAME = "ShareMind AI"

APP_VERSION = "1.0.0"
