import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

def cors_permit():

    FRONTEND_URL1 = os.getenv('FRONTEND_URL1')
    FRONTEND_URL2 = os.getenv('FRONTEND_URL2')

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
