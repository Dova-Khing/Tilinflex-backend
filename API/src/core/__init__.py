"""
Núcleo de la API: excepciones y estructuras de respuesta estándar.
"""

from API.src.core.exceptions import (
    AppException,
    BadRequestError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from API.src.core.responses import (
    ApiErrorDetail,
    ApiErrorResponse,
    ApiResponse,
    error_response,
    success_response,
)

__all__ = [
    "AppException",
    "BadRequestError",
    "ConflictError",
    "NotFoundError",
    "ValidationError",
    "ApiErrorDetail",
    "ApiErrorResponse",
    "ApiResponse",
    "error_response",
    "success_response",
]
