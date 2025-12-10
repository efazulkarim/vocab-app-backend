import json
from typing import Any, Dict

from groq import Groq

from app.core.config import settings
from app.core.exceptions import AIError

SYSTEM_PROMPT = (
    "You are a vocabulary teacher. Return JSON with definition, mnemonic, sentence, synonyms. No markdown."
)


class AIRepository:
    """Repository responsible for generating vocabulary details via Groq."""

    def __init__(self) -> None:
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        except Exception as exc:  # pragma: no cover - defensive guard
            raise AIError(f"Failed to initialize Groq client: {exc}") from exc

    def generate_word_details(self, word: str) -> Dict[str, Any]:
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": word},
                ],
                response_format={"type": "json_object"},
            )
        except Exception as exc:
            raise AIError(f"Groq request failed: {exc}") from exc

        try:
            raw_content = completion.choices[0].message.content
        except (AttributeError, IndexError, KeyError) as exc:
            raise AIError("Groq response was missing content") from exc

        if not raw_content:
            raise AIError("Groq response was empty")

        try:
            data = json.loads(raw_content)
        except Exception as exc:
            raise AIError(f"Failed to parse Groq JSON response: {exc}") from exc

        synonyms = data.get("synonyms") or []
        if not isinstance(synonyms, list):
            synonyms = [str(synonyms)]

        normalized_synonyms = [str(item).strip() for item in synonyms if str(item).strip()]

        return {
            "definition": str(data.get("definition", "")).strip(),
            "mnemonic": str(data.get("mnemonic", "")).strip(),
            "sentence": str(data.get("sentence", "")).strip(),
            "synonyms": normalized_synonyms[:3],
        }

