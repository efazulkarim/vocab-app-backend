from typing import List

from pydantic import BaseModel, Field, field_validator


class WordRequest(BaseModel):
    word: str = Field(..., min_length=1)

    @field_validator("word")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("word must not be empty")
        return cleaned


class WordResponse(BaseModel):
    word: str
    definition: str
    mnemonic: str
    sentence: str
    synonyms: List[str] = Field(default_factory=list, max_length=3)
    is_cached: bool

    @field_validator("synonyms")
    @classmethod
    def normalize_synonyms(cls, value: List[str]) -> List[str]:
        cleaned = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        return cleaned[:3]

