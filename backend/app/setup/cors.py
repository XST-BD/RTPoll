from dotenv import load_dotenv
import os


from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware

from .vars import app, SECRET_KEY

load_dotenv()
FRONTEND_URL_LOCAL = os.getenv("FRONTEND_URL_LOCAL")
FRONTEND_URL_NETWORK1 = os.getenv("FRONTEND_URL_NETWORK")
FRONTEND_URL_NETWORK2 = os.getenv("FRONTEND_URL_NETWORK")

def cors_permit():

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(FRONTEND_URL_LOCAL), str(FRONTEND_URL_NETWORK1), str(FRONTEND_URL_NETWORK2)],
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