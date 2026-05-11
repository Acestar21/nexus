import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import dashboard
from app.db import init_db

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MCP Dashboard backend...")
    logger.info(f"ollama_host: {settings.ollama_host}")
    logger.info(f"ollama_model: {settings.ollama_model}")
    init_db()
    yield
    logger.info("Shutting down MCP Dashboard backend...")

app = FastAPI(
    title = "Nexus Dashboard API",
    version = "0.1.0",
    lifespan = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/health")
async def health():
    return {"status": "ok"}