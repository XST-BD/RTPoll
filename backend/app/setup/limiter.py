from fastapi import Request
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .vars import app

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Custom handler for rate limiter
async def rate_limit_handler(request: Request, exc: Exception):
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )
    raise exc

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
