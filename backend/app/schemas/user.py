from datetime import date
from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):

    name : str
    email: str
    password: str
    fingerprint: str


class UserView(BaseModel):

    name : str
    creation_date: date

    class Config:
        from_attributes = True   # REQUIRED for SQLAlchemy