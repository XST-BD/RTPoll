from fastapi.responses import JSONResponse

def api_error(message: str, field: str | None = None, status_code: int = 400):
    """
    Standardized error response for all endpoints.
    - message: human-readable error
    - field: optional, for form validation
    - status_code: HTTP status
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "field": field,
            "message": message
        }
    )