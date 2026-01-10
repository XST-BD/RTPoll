from datetime import date
from typing import List
from uuid import UUID

from sqlalchemy import (
    Column, Row, Integer, Float, String, Boolean, JSON, Date, func
)
from sqlalchemy.orm import relationship

from app.db.base import Base

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    fingerprint = Column(String, nullable=True)     # stores user uniquness using fingerprintJS
    creation_date = Column(Date, nullable=False, default=date.today())

    # relationship to PollModel (polls get deleted with user if user is deleted)
    polls = relationship("PollModel", back_populates="creator", cascade="all, delete-orphan")
