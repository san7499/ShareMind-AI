from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routes.chat import router as chat_router
from app.routes.sync import router as sync_router
from app.routes.health import router as health_router

app = FastAPI(
    title="ShareMind AI",
    description="Enterprise SharePoint Permission-Aware RAG Chatbot",
    version="1.0.0"
)

# Register Routes
app.include_router(chat_router)
app.include_router(sync_router)
app.include_router(health_router)


@app.get("/")
def home():
    return JSONResponse(
        {
            "project": "ShareMind AI",
            "status": "Running",
            "version": "1.0.0"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )