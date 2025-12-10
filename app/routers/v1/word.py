from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import AppException
from app.schemas.word import WordRequest, WordResponse
from app.services.vocab_service import VocabService

router = APIRouter(prefix="/word", tags=["vocabulary"])


@router.post("/generate", response_model=WordResponse, status_code=status.HTTP_200_OK)
def generate_word(
    request: WordRequest,
    service: VocabService = Depends(VocabService),
) -> WordResponse:
    try:
        return service.get_or_create_word(request.word)
    except AppException as exc:
        raise exc.to_http_exception() from exc
    except Exception as exc:  # pragma: no cover - safety net
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

