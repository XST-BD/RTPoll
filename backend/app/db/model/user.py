from datetime import datetime, date, timedelta, timezone
import uuid

from sqlalchemy import (
    Column, Integer, String, Date, DateTime, func, UniqueConstraint,JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserModel(Base):

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(36),                                 # UUID as string
        primary_key=True, index=True, unique=True,
        default=lambda: str(uuid.uuid4())           # auto-generate
    )

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    creation_date: Mapped[datetime] = mapped_column(Date, nullable=False, default=date.today)

    # relationship to PollModel (polls get deleted with user if user is deleted)
    polls = relationship('PollModel', back_populates="creator", cascade="all, delete-orphan")


class EmailVerification(Base):

    __tablename__ = "email_verifications"
    __table_args__ = (
        UniqueConstraint('email', 'token_type', name='uq_email_token_type'),
    )

    id = Column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
    token_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String, index=True, nullable=False)
    extra_data: Mapped[str] = mapped_column(JSON, nullable=True)
    used: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    