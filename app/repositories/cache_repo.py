import json
from typing import Any, Dict, Optional

from upstash_redis import Redis

from app.core.config import settings
from app.core.exceptions import CacheError

DEFAULT_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 days


class CacheRepository:
    """Repository responsible for interacting with Upstash Redis."""

    def __init__(self) -> None:
        try:
            self.client = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
        except Exception as exc:  # pragma: no cover - defensive guard
            raise CacheError(f"Failed to initialize Redis client: {exc}") from exc

    @staticmethod
    def _key(word: str) -> str:
        return f"vocab:{word}"

    def get_word(self, word: str) -> Optional[Dict[str, Any]]:
        try:
            raw_value = self.client.get(self._key(word))
        except Exception as exc:
            raise CacheError(f"Error fetching word from cache: {exc}") from exc

        if raw_value is None:
            return None

        try:
            return json.loads(raw_value)
        except Exception as exc:
            raise CacheError(f"Failed to decode cached payload: {exc}") from exc

    def save_word(self, word: str, data: Dict[str, Any], expire: int = DEFAULT_TTL_SECONDS) -> None:
        try:
            payload = json.dumps(data)
            self.client.set(self._key(word), payload, ex=expire)
        except Exception as exc:
            raise CacheError(f"Error saving word to cache: {exc}") from exc

