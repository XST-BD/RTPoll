import uuid

from sqlalchemy import String, JSON, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

from app.db.base import Base 

class PollModel(Base):

    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    options = Column(JSON, nullable=False)

    creator = relationship('UserModel', back_populates='polls')
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    expires_at = Column(DateTime, nullable=False)