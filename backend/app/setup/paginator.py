from fastapi_pagination import Params, add_pagination

from .vars import app

class CustomParams(Params):
    size: int = 20
    max_size: int = 100

add_pagination(app)