# ShareMind AI

## Enterprise Open WebUI Chatbot with SharePoint Permission-Aware RAG

ShareMind AI is an enterprise knowledge assistant that integrates Microsoft SharePoint Online with Open WebUI using Microsoft Graph API and Retrieval-Augmented Generation (RAG).

The application synchronizes SharePoint documents, creates vector embeddings, performs semantic search, and generates answers using an open-source Large Language Model (LLM) while providing citations from SharePoint documents.

---

## Features

- Microsoft Entra ID Authentication
- Microsoft Graph API Integration
- SharePoint Document Synchronization
- PDF and DOCX Parsing
- Text Chunking
- Embedding Generation
- ChromaDB Vector Database
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Ollama LLM Integration
- Source Citations
- REST APIs using FastAPI

---

## Tech Stack

- Python
- FastAPI
- Microsoft Graph API
- Microsoft Entra ID
- ChromaDB
- Sentence Transformers
- Ollama
- Open WebUI
- LangChain
- PyMuPDF
- python-docx

---

## Project Structure

```
ShareMind-AI/
│
├── app/
├── data/
├── scripts/
├── tests/
├── screenshots/
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ShareMind-AI.git

cd ShareMind-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

Example:

```env
TENANT_ID=xxxxxxxx

CLIENT_ID=xxxxxxxx

CLIENT_SECRET=xxxxxxxx

SHAREPOINT_SITE_ID=xxxxxxxx

SHAREPOINT_DRIVE_ID=xxxxxxxx

OLLAMA_MODEL=llama3
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## Future Enhancements

- Permission-Aware Retrieval
- OCR Support
- Delta Synchronization
- Hybrid Search
- Multi-turn Conversation Memory
- Audit Logging
- Docker Deployment

---

## Author

Sanket Khapake

