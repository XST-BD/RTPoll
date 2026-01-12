from datetime import date
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, field_validator 
from typing import List
import re

from typing_extensions import Annotated

UsernameStr = Annotated[
    str,
    Field(min_length=3, max_length=30)
]

class UserCreate(BaseModel):

    username : UsernameStr
    email: str
    password: str


    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[A-Za-z0-9_]+$', v):
            raise ValueError(
                "Username should only contain alphabets, numbers and underscores"
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        try:
            validate_email(v)
        except EmailNotValidError:
            raise ValueError("Wrong email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserView(BaseModel):

    username : str
    creation_date: date

    class Config:
        from_attributes = True   # REQUIRED for SQLAlchemy