from fastapi import Depends

from app.core.exceptions import ServiceError
from app.repositories.ai_repo import AIRepository
from app.repositories.cache_repo import CacheRepository
from app.schemas.word import WordResponse


class VocabService:
    """Business logic for fetching and caching vocabulary data."""

    def __init__(
        self,
        cache_repo: CacheRepository = Depends(CacheRepository),
        ai_repo: AIRepository = Depends(AIRepository),
    ) -> None:
        self.cache_repo = cache_repo
        self.ai_repo = ai_repo

    def get_or_create_word(self, word: str) -> WordResponse:
        normalized_word = word.strip().lower()
        if not normalized_word:
            raise ServiceError("Word must not be empty")

        cached = self.cache_repo.get_word(normalized_word)
        if cached:
            cached_data = {**cached, "word": normalized_word, "is_cached": True}
            return WordResponse(**cached_data)

        ai_data = self.ai_repo.generate_word_details(normalized_word)
        self.cache_repo.save_word(normalized_word, ai_data)

        response_data = {**ai_data, "word": normalized_word, "is_cached": False}
        return WordResponse(**response_data)

