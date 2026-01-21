import os

from datetime import timedelta, datetime

from dotenv import load_dotenv

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 

from starlette.middleware.sessions import SessionMiddleware

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


app = FastAPI()
router = APIRouter()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Custom handler
async def rate_limit_handler(request: Request, exc: Exception):
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )
    raise exc

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

load_dotenv()

BACKEND_URL1 = os.getenv('BACKEND_URL1')
FRONTEND_URL = os.getenv('FRONTEND_ORIGINS')
DATABASE_URL = os.getenv('DATABASE_URL')
SENDER_MAIL = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
APP_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
SMTP_SERVER = os.getenv('MAIL_SERVER')
SMTP_PORT_TLS = os.getenv('MAIL_PORT_TLS', 587)

SESSION_TTL = timedelta(days=7)

FRONTEND_ORIGINS = [
    o.rstrip("/")
    for o in os.getenv("FRONTEND_ORIGINS", "").split(",")
    if o
]

def cors_permit():

    app.add_middleware(
        CORSMiddleware,
        allow_origins=FRONTEND_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware, 
        session_cookie='session',
        secret_key=str(SECRET_KEY),
        max_age=60*60*24*7,            # 1 week
        https_only=False,  # must be False on localhost HTTP
        same_site="lax",  # allows cross-site JS requests to send cookie
    )