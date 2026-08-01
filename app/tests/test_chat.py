from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_success():
    """Test that a valid question returns HTTP 200 with an 'answer' and a list of 'sources'."""
    response = client.post(
        "/chat",
        json={"question": "What is the company policy on remote work?"}
    )
    
    # Assert successful HTTP response
    assert response.status_code == 200
    
    # Assert proper content type is returned
    assert response.headers["content-type"].startswith("application/json")
    
    data = response.json()
    
    # Assert expected enterprise RAG response structure fields are present
    assert "answer" in data
    assert "sources" in data
    
    # Verify data types and content validation
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
    assert isinstance(data["sources"], list)


def test_chat_empty_question():
    """Test that an empty question payload returns a validation error (HTTP 422).
    
    Requires Pydantic validation on the ChatRequest model:
    question: str = Field(..., min_length=1)
    """
    response = client.post(
        "/chat",
        json={"question": ""}
    )
    
    # FastAPI/Pydantic validation failure status code for min_length constraint
    assert response.status_code == 422


def test_chat_missing_question_field():
    """Test that a request missing the 'question' key entirely returns a validation error (HTTP 422)."""
    response = client.post(
        "/chat",
        json={}
    )
    
    assert response.status_code == 422