from fastapi import Request, status
from fastapi.responses import JSONResponse

class ComplaintPriorityError(Exception):
    """Base exception for all system errors."""
    pass

class ComplaintNotFoundError(ComplaintPriorityError):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Complaint not found: {identifier}")

class DuplicateComplaintError(ComplaintPriorityError):
    def __init__(self, original_id: str):
        self.original_id = original_id
        super().__init__(f"Duplicate complaint detected. Original: {original_id}")

class AuthenticationError(ComplaintPriorityError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)

class AuthorizationError(ComplaintPriorityError):
    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(message)

class ValidationError(ComplaintPriorityError):
    def __init__(self, message: str):
        super().__init__(message)

class AIAnalysisError(ComplaintPriorityError):
    def __init__(self, message: str = "AI analysis failed"):
        super().__init__(message)

class ConfigurationError(ComplaintPriorityError):
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)

# FastAPI Exception Handlers
async def complaint_not_found_handler(request: Request, exc: ComplaintNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

async def auth_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})
