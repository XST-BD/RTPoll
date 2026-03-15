import os

from datetime import timedelta, datetime
from dotenv import load_dotenv

from fastapi import FastAPI, APIRouter

from app.setup.lifespan import lifespan

load_dotenv()

ENV = os.getenv("ENVIRONMENT", "development")
BACKEND_URL1 = os.getenv('BACKEND_URL1')
FRONTEND_URL_LOCAL = os.getenv('FRONTEND_URL_LOCAL')
SENDER_MAIL = os.getenv('MAIL_USERNAME', 'MAIL_USERNAME')
APP_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
SMTP_SERVER = os.getenv('MAIL_SERVER')
SMTP_PORT_TLS = os.getenv('MAIL_PORT_TLS', 587)

SESSION_TTL = timedelta(days=7)

app = FastAPI(lifespan=lifespan)
router = APIRouter()

