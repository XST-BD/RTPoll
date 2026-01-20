import os

from datetime import timedelta, datetime

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

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

    # origins = [
    #     o.strip()
    #     for o in os.getenv("FRONTEND_ORIGINS", "").split(",")
    #     if o
    # ]

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