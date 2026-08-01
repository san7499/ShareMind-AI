# ShareMind AI

# Enterprise Open WebUI Chatbot with SharePoint Permission-Aware RAG

ShareMind AI is an enterprise-grade chatbot that integrates **Microsoft SharePoint Online** with **Microsoft Graph API**, **Retrieval-Augmented Generation (RAG)**, and **Ollama LLM** to provide secure, intelligent document-based question answering.

The application synchronizes SharePoint documents, extracts and indexes their content, generates vector embeddings, performs semantic search using ChromaDB, and produces context-aware responses with source citations.

---

# Features

- Microsoft Entra ID Authentication
- Microsoft Graph API Integration
- SharePoint Document Synchronization
- PDF, DOCX, TXT Document Parsing
- Text Chunking
- Embedding Generation using Sentence Transformers
- ChromaDB Vector Database
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Ollama LLM Integration
- Source Citation Support
- FastAPI REST APIs
- Interactive Web UI
- Health Monitoring API
- Document Synchronization API

---

# Tech Stack

## Backend

- Python
- FastAPI
- Microsoft Graph API
- Microsoft Entra ID (Azure AD)
- ChromaDB
- Sentence Transformers
- Ollama
- LangChain

## Document Processing

- PyMuPDF
- python-docx

## Frontend

- HTML
- CSS
- JavaScript
- Bootstrap 5

---

# Project Structure

```text
ShareMind-AI/
│
├── app/
│   ├── data/
│   ├── models/
│   ├── routes/
│   ├── scripts/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── tests/
│   ├── utils/
│   ├── config.py
│   └── main.py
│
├── data/
│   ├── chroma_db/
│   ├── documents/
│   └── embeddings/
│
├── logs/
├── screenshots/
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── .env
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/ShareMind-AI.git

cd ShareMind-AI
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
TENANT_ID=xxxxxxxxxxxxxxxx

CLIENT_ID=xxxxxxxxxxxxxxxx

CLIENT_SECRET=xxxxxxxxxxxxxxxx

SHAREPOINT_SITE_ID=xxxxxxxxxxxxxxxx

SHAREPOINT_DRIVE_ID=xxxxxxxxxxxxxxxx

GRAPH_BASE_URL=https://graph.microsoft.com/v1.0

OLLAMA_URL=http://localhost:11434

OLLAMA_MODEL=llama3

CHROMA_DB_PATH=./data/chroma_db

DOCUMENT_FOLDER=./data/documents
```

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

---

## Application URLs

### Home

```
http://127.0.0.1:8000/
```

### Web UI

```
http://127.0.0.1:8000/ui
```

### Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

### ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Home Endpoint |
| GET | `/health` | Health Check |
| POST | `/chat` | Ask Questions |
| POST | `/sync` | Synchronize SharePoint Documents |
| GET | `/ui` | Web User Interface |

---

# RAG Pipeline

```
User Question
      │
      ▼
FastAPI Chat API
      │
      ▼
Embedding Generation
      │
      ▼
ChromaDB Semantic Search
      │
      ▼
Relevant SharePoint Chunks
      │
      ▼
Prompt Construction
      │
      ▼
Ollama LLM
      │
      ▼
Generated Answer
      │
      ▼
Source Citations
```

---

# Current Capabilities

- SharePoint Integration
- Document Parsing
- Text Chunking
- Vector Embedding
- ChromaDB Storage
- Semantic Search
- RAG Pipeline
- Ollama Integration
- REST APIs
- Web Interface

---

# Future Enhancements

- Permission-Aware Retrieval
- Incremental (Delta) Synchronization
- OCR Support
- Hybrid Search (Keyword + Vector)
- Multi-turn Conversation Memory
- Document Version Tracking
- Audit Logging
- Docker Deployment
- Kubernetes Deployment
- CI/CD Pipeline
- Redis Caching
- JWT Authentication
- Multi-user Support

---

# Screenshots

Place project screenshots inside the `screenshots/` directory.

Example:

```
screenshots/

home.png

chat.png

sync.png

swagger.png

architecture.png
```

---

# License

This project is licensed under the MIT License.

---

# Author

**Sanket Khapake**

- GitHub: https://github.com/san7499
- LinkedIn: https://www.linkedin.com/in/sanket-khapake

---

# Acknowledgements

- Microsoft Graph API
- Microsoft Entra ID
- FastAPI
- ChromaDB
- Sentence Transformers
- Ollama
- LangChain
- Bootstrap