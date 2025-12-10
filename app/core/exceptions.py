from fastapi import HTTPException, status


class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=self.status_code, detail=self.detail)


class RepositoryError(AppException):
    """Base exception for repository layer errors."""


class CacheError(RepositoryError):
    """Raised when cache operations fail."""

    def __init__(self, detail: str = "Cache operation failed", status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE) -> None:
        super().__init__(detail, status_code)


class AIError(RepositoryError):
    """Raised when the AI provider returns an error."""

    def __init__(self, detail: str = "AI generation failed", status_code: int = status.HTTP_502_BAD_GATEWAY) -> None:
        super().__init__(detail, status_code)


class ServiceError(AppException):
    """Raised when the service layer encounters an unrecoverable error."""

