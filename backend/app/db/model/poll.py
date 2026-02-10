from datetime import datetime
import uuid

from sqlalchemy import Boolean, String, JSON, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

from app.db.base import Base 

class PollModel(Base):

    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    options = Column(JSON, nullable=False)
    votes = Column(JSON, default=dict)

    creator = relationship('UserModel', back_populates='polls')
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    is_indefinite: Mapped[bool] = mapped_column(default=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)