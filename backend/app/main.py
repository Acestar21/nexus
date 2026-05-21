import logging
import httpx
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


async def check_ollama_health():
    if not settings.enable_ai_brief:
        logger.info("AI brief disabled, skipping Ollama check")
        return True
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.ollama_host}/api/tags")
            if response.status_code == 200:
                logger.info("✓ Ollama is running and healthy")
                return True
    except Exception as e:
        logger.warning(f"⚠ Ollama not detected: {e}")
        logger.warning(f"  AI brief is enabled but Ollama is not available at {settings.ollama_host}")
        logger.warning(f"  Either start Ollama or set ENABLE_AI_BRIEF=false")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting NEXUS...")
    await check_ollama_health()
    init_db()
    yield
    logger.info("Shutting down NEXUS")

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