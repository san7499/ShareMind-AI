"""
main.py

Entry point for the ShareMind AI application.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routes.chat import router as chat_router
from app.routes.sync import router as sync_router
from app.routes.health import router as health_router

from app.utils.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(
    title="ShareMind AI",
    description="Enterprise SharePoint Permission-Aware RAG Chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# -----------------------------------------------------
# Startup Event
# -----------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting ShareMind AI...")
    logger.info("Application started successfully.")


# -----------------------------------------------------
# Shutdown Event
# -----------------------------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ShareMind AI...")


# -----------------------------------------------------
# Register API Routes
# -----------------------------------------------------
app.include_router(
    chat_router,
    tags=["Chat"]
)

app.include_router(
    sync_router,
    tags=["SharePoint"]
)

app.include_router(
    health_router,
    tags=["Health"]
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get(
    "/ui",
    tags=["UI"],
    summary="ShareMind AI Web Interface"
)
async def ui(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
# -----------------------------------------------------
# Root Endpoint
# -----------------------------------------------------
@app.get("/", tags=["Home"])
async def home():
    """
    Root endpoint.
    """

    return JSONResponse(
        status_code=200,
        content={
            "project": "ShareMind AI",
            "description": "Enterprise Open WebUI Chatbot with SharePoint Permission-Aware RAG",
            "version": "1.0.0",
            "status": "Running",
            "documentation": "/docs"
        }
    )


# -----------------------------------------------------
# Run Application
# -----------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )