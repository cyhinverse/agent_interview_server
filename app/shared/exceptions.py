from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    """Base exception for all application-specific errors."""
    def __init__(
        self, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail: str = "An unexpected error occurred",
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BaseAppException):
    """Raised when a requested resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationException(BaseAppException):
    """Raised when input data validation fails."""
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DuplicatedEntityException(BaseAppException):
    """Raised when trying to create an entity that already exists."""
    def __init__(self, detail: str = "Entity already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnauthorizedException(BaseAppException):
    """Raised when authentication is required or fails."""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(BaseAppException):
    """Raised when a user is authenticated but not authorized to perform an action."""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class DomainException(BaseAppException):
    """Raised when a domain-specific error occurs."""
    def __init__(self, detail: str = "Domain-specific error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
