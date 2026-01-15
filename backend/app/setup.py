import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()

BACKEND_URL1 = os.getenv('BACKEND_URL1')
FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
FRONTEND_URL2 = os.getenv('FRONTEND_URL2')
DATABASE_URL = os.getenv('DATABASE_URL')
SENDER_MAIL = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
APP_PASSWORD = os.getenv('MAIL_PASSWORD')
SMTP_SERVER = os.getenv('MAIL_SERVER')
SMTP_PORT_TLS = os.getenv('MAIL_PORT_TLS', 587)


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
