import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

OLLAMA_ENDPOINT = f"{settings.ollama_host}/api/generate"


def build_prompt(github: dict, fitness: dict, leetcode: dict) -> str:
    return f"""You are a personal productivity assistant giving a brief morning summary.
Be concise, direct, and analytical. No generic motivation. Max 4 sentences.
You generate concise operational summaries from developer activity telemetry.

Your tone must be:
- analytical
- observational
- direct
- calm

Do NOT:
- motivate the user
- praise the user
- sound like a life coach
- use generic productivity advice
- invent insights not supported by the data

Avoid phrases like:
- "Keep it up"
- "Stay consistent"
- "Great work"
- "Small wins"
- "You got this"
- "Consistency is key"

Focus on:
- activity changes
- streak status
- inactivity
- workload balance
- notable signals
- short-term comparisons

Maximum 4 sentences.

Current Operational State:

GitHub:
- Commits today: {github["activity"]["commits_today"]}
- Commits this week: {github["activity"]["commits_this_week"]}
- Current streak: {github["activity"]["current_streak"]} days
- Last commit date: {github["activity"]["last_commit_date"]}

LeetCode:
- Problems solved today: {leetcode["activity"]["problem_solved_today"]}
- Problems solved this week: {leetcode["activity"]["problem_solved_this_week"]}
- Current streak: {leetcode["activity"]["current_streak"]} days
- Total solved: {leetcode["activity"]["total_problem_solved"]}

Fitness:
- Workout completed today: {fitness["worked_out_today"]}
- Current workout streak: {fitness["current_streak"]} days
- Workouts this week: {fitness["total_workouts_this_week"]}

Generate the operational summary.
"""


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
    