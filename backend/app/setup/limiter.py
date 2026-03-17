from fastapi import Request
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.services.auth import decode_token
from app.setup.vars import app

def user_key_func(request: Request):
    auth = request.headers.get("authorization")

    if auth:
        parts = auth.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            try:
                payload = decode_token(parts[1])
                return f"user:{payload['user_id']}"
            except Exception:
                pass

        # Try refresh token
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            try:
                payload = decode_token(refresh_token)
                return f"user:{payload['user_id']}"
            except Exception:
                pass
    
    return f"ip:{get_remote_address(request)}"

limiter = Limiter(key_func=user_key_func)
app.state.limiter = limiter

# Custom handler for rate limiter
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: Exception):

    retry_after = getattr(exc, "retry_after", 60)
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
        headers={"Retry-After": str(retry_after)}
    )

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
