from datetime import date
from typing import List
import uuid

from sqlalchemy import (
    Column, Row, Integer, Float, String, Boolean, JSON, Date, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base

class UserModel(Base):

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(36),                                 # UUID as string
        primary_key=True, index=True, unique=True,
        default=lambda: str(uuid.uuid4())           # auto-generate
    )

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    creation_date = Column(Date, nullable=False, default=date.today())

    # relationship to PollModel (polls get deleted with user if user is deleted)
    # polls = relationship("PollModel", back_populates="creator", cascade="all, delete-orphan")


class EmailVerification(Base):

    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    token_hash = Column(String, index=True)
    used: Mapped[bool] = mapped_column(default=False)

    