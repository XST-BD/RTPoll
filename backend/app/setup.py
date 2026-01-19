import os

from datetime import timedelta, datetime

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

load_dotenv()

BACKEND_URL1 = os.getenv('BACKEND_URL1')
FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
FRONTEND_URL2 = os.getenv('FRONTEND_URL2')
DATABASE_URL = os.getenv('DATABASE_URL')
SENDER_MAIL = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
APP_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
SMTP_SERVER = os.getenv('MAIL_SERVER')
SMTP_PORT_TLS = os.getenv('MAIL_PORT_TLS', 587)

SESSION_TTL = timedelta(days=7)

def cors_permit():

    origins = [
        FRONTEND_URL1,
        FRONTEND_URL2
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=str(origins),
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
        same_site="none",  # allows cross-site JS requests to send cookie
    )