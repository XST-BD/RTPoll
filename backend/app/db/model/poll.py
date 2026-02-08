import uuid

from sqlalchemy import String, JSON, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

from app.db.base import Base 

class PollModel(Base):

    __tablename__ = "polls"

    poll_id: Mapped[str] = mapped_column(
        String(36),                                 # UUID as string
        primary_key=True, index=True, unique=True,
        default=lambda: str(uuid.uuid4())           # auto-generate
    )
    title: Mapped[str] = mapped_column(nullable=False)
    options = Column(JSON, nullable=False)

    creator = relationship('UserModel', back_populates='polls')
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    expires_at = Column(DateTime, nullable=False)