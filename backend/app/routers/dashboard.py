import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.mcp_client import call_tool
from app.ollama_client import generate_brief
from app.db import get_connection

logger = logging.getLogger(__name__)

router = APIRouter()


def save_snapshot(source: str, data: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO metric_snapshots (source, captured_at, data) VALUES (?, ?, ?)",
            (source, datetime.now(timezone.utc).isoformat(), json.dumps(data)),
        )


def save_brief(brief: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO daily_briefs (created_at, brief) VALUES (?, ?)",
            (datetime.now(timezone.utc).isoformat(), brief),
        )


@router.get("/summary")
async def get_summary():
    try:
        logger.info("Fetching data from MCP servers...")
        github_data = await call_tool("github", "get_github_activity")
        fitness_data = await call_tool("fitness", "get_fitness_activity")

        save_snapshot("github", github_data)
        save_snapshot("fitness", fitness_data)

        brief = await generate_brief(github_data, fitness_data)
        save_brief(brief)

        return {
            "github": github_data,
            "fitness": fitness_data,
            "brief": brief,
        }
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))