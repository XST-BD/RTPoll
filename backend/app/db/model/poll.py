from sqlmodel import SQLModel, Field
from typing import List

from sqlalchemy import (
    Integer, Float, Boolean, String, Column, Row, JSON
)

from app.db.base import Base

class PollModel(Base):

    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)

