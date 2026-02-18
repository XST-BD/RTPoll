import os

from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware

from .vars import app, SECRET_KEY

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

    # app.add_middleware(
    #     SessionMiddleware, 
    #     session_cookie='session',
    #     secret_key=str(SECRET_KEY),
    #     max_age=60*60*24*7,            # 1 week
    #     https_only=False,  # must be False on localhost HTTP
    #     same_site="lax",  # allows cross-site JS requests to send cookie
    # )