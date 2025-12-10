from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GROQ_API_KEY: str = Field(..., description="API key for Groq")
    UPSTASH_REDIS_REST_URL: str = Field(..., description="Upstash REST URL")
    UPSTASH_REDIS_REST_TOKEN: str = Field(..., description="Upstash REST token")


settings = Settings()

