from datetime import datetime, timezone
import uuid

from sqlalchemy import Boolean, String, JSON, Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Dict

from app.db.base import Base 

class PollModel(Base):

    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    options: Mapped[list[str]] = mapped_column(JSON, default=list)
    votes: Mapped[list[int]] = mapped_column(JSON, default=list)

    creator = relationship('UserModel', back_populates='polls')
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    is_indefinite: Mapped[bool] = mapped_column(default=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())