from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ==========================================
# 1. Base & Domain-Specific Exceptions
# ==========================================

class BaseAuditorException(Exception):
    """Base exception for all domain errors in the Insurance Auditor."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class PolicyDataNotFoundError(BaseAuditorException):
    """Raised when the agent cannot locate official policy documentation online."""
    def __init__(self, message: str = "Unable to locate official policy guidelines for the specified provider/product."):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class ToolExecutionError(BaseAuditorException):
    """Raised when an external tool (e.g., Tavily search, web scraper) fails."""
    def __init__(self, message: str = "A tool execution error occurred during policy data retrieval."):
        super().__init__(message=message, status_code=status.HTTP_502_BAD_GATEWAY)


class ScoreParsingError(BaseAuditorException):
    """Raised when the LLM outputs an invalid JSON payload or fails schema validation."""
    def __init__(self, message: str = "Failed to parse the auditor's evaluation into the expected score schema."):
        super().__init__(message=message, status_code=status.HTTP_502_BAD_GATEWAY)


class AgentTimeoutError(BaseAuditorException):
    """Raised when the LangGraph agent exceeds the maximum allowed execution time/cycles."""
    def __init__(self, message: str = "The auditing agent exceeded the allowed time limit."):
        super().__init__(message=message, status_code=status.HTTP_504_GATEWAY_TIMEOUT)


# ==========================================
# 2. Global FastAPI Exception Handlers
# ==========================================

def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers custom exception handlers with the FastAPI application instance.
    """
    @app.exception_handler(BaseAuditorException)
    async def auditor_exception_handler(request: Request, exc: BaseAuditorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_type": exc.__class__.__name__,
                "detail": exc.message,
            },
        )