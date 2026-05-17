import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

OLLAMA_ENDPOINT = f"{settings.ollama_host}/api/generate"


def build_prompt(github: dict, fitness: dict, leetcode: dict) -> str:
    return f"""You are a personal productivity assistant giving a brief morning summary.
Be concise, direct, and analytical. No generic motivation. Max 4 sentences.
Compare to recent trends where possible.

GitHub:
- Commits today: {github["activity"]["commits_today"]}
- Commits this week: {github["activity"]["commits_this_week"]}
- Current streak: {github["activity"]["current_streak"]} days
- Last commit: {github["activity"]["last_commit_date"]}

LeetCode:
- Problems solved today: {leetcode["activity"]["problem_solved_today"]}
- Problems solved this week: {leetcode["activity"]["problem_solved_this_week"]}
- Current streak: {leetcode["activity"]["current_streak"]} days
- Total solved: {leetcode["activity"]["total_problem_solved"]}

Fitness:
- Worked out today: {fitness["worked_out_today"]}
- Current streak: {fitness["current_streak"]} days
- Workouts this week: {fitness["total_workouts_this_week"]}

Give a short morning brief based on this data."""


async def generate_brief(github: dict, fitness: dict, leetcode: dict) -> str:
    prompt = build_prompt(github, fitness, leetcode)
    logger.info("Generating daily brief with Ollama...")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OLLAMA_ENDPOINT,
            json={
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]
    