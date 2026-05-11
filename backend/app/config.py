from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # GitHub
    github_token: str = Field(..., description="GitHub personal access token")

    # LeetCode
    leetcode_username: str = Field(..., description="LeetCode username")
    leetcode_session_cookie: str = Field(..., description = "LeetCode session cookie")

    fitness_log_path: str = Field(default="./data/fitness.json")

    # Ollama
    ollama_host: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.2")

    # Backend
    backend_port: int = Field(default=8000)


settings = Settings()