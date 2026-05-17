import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.mcp_client import call_tool
from app.ollama_client import generate_brief
from app.db import get_connection
from pydantic import BaseModel
from datetime import datetime, timezone, date


logger = logging.getLogger(__name__)

router = APIRouter()

class WorkoutLog(BaseModel):
    date: str
    completed: bool
    duration_minutes: int | None = None
    notes: str | None = None

def get_todays_brief() -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT brief FROM daily_briefs WHERE DATE(created_at) = DATE('now') ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        return row["brief"] if row else None


def save_brief(brief: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO daily_briefs (created_at, brief) VALUES (?, ?)",
            (datetime.now(timezone.utc).isoformat(), brief),
        )

def save_snapshot(source: str, data: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO metric_snapshots (source, captured_at, data) VALUES (?, ?, ?)",
            (source, datetime.now(timezone.utc).isoformat(), json.dumps(data)),
        )


@router.get("/summary")
async def get_summary():
    try:
        github_data = await call_tool("github", "get_github_activity")
        fitness_data = await call_tool("fitness", "get_fitness_activity")
        leetcode_data = await call_tool("leetcode", "get_leetcode_activity")

        save_snapshot("github", github_data)
        save_snapshot("fitness", fitness_data)
        save_snapshot("leetcode", leetcode_data)

        brief = get_todays_brief()
        if not brief:
            brief = await generate_brief(github_data, fitness_data, leetcode_data)
            save_brief(brief)

        return {
            "github": github_data,
            "fitness": fitness_data,
            "leetcode": leetcode_data,
            "brief": brief,
        }
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/log-workout")
async def log_workout(payload: WorkoutLog):
    try:
        result = await call_tool("fitness", "log_workout", payload.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error logging workout: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh-brief")
async def refresh_brief():
    try:
        github_data = await call_tool("github", "get_github_activity")
        fitness_data = await call_tool("fitness", "get_fitness_activity")
        leetcode_data = await call_tool("leetcode", "get_leetcode_activity")
        brief = await generate_brief(github_data, fitness_data, leetcode_data)
        save_brief(brief)
        return {"github": github_data, "fitness": fitness_data, "leetcode": leetcode_data, "brief": brief}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))