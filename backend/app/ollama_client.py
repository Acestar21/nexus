import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

OLLAMA_ENDPOINT = f"{settings.ollama_host}/api/generate"


def build_prompt(github: dict, fitness: dict) -> str:
    return f"""You are a personal productivity assistant giving a brief morning summary.
Be concise, direct, and specific. No generic motivation. Max 4 sentences.

Here is today's data:

GitHub:
- Commits today: {github["activity"]["commits_today"]}
- Commits this week: {github["activity"]["commits_this_week"]}
- Current streak: {github["activity"]["current_streak"]} days
- Last commit: {github["activity"]["last_commit_date"]}

Fitness:
- Worked out today: {fitness["worked_out_today"]}
- Current streak: {fitness["current_streak"]} days
- Workouts this week: {fitness["total_workouts_this_week"]}
- Last workout: {fitness["last_workout_date"]}

Give a short morning brief based on this data."""


async def generate_brief(github: dict, fitness: dict) -> str:
    prompt = build_prompt(github, fitness)
    logger.info("Generating daily brief with Ollama...")

    async with httpx.AsyncClient(timeout=60.0) as client:
        logger.info(f"Hitting Ollama at: {OLLAMA_ENDPOINT}")
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
    

if __name__ == "__main__":
    import asyncio
    async def test():
        result = await generate_brief(
            {"activity": {"commits_today": 2, "commits_this_week": 8, "current_streak": 3, "last_commit_date": "2026-05-12"}},
            {"worked_out_today": True, "current_streak": 1, "total_workouts_this_week": 1, "last_workout_date": "2026-05-12"}
        )
        print(result)
    asyncio.run(test())