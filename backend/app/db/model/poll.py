from datetime import datetime, timezone
import nanoid

from sqlalchemy import Boolean, String, JSON, Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Dict

from app.db.base import Base 

class PollOption(Base):
    __tablename__ = "poll_options"
    __table_args__ = (UniqueConstraint("poll_id", "position"),)

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(
        String(18), 
        primary_key=True, index=True, unique=True,
        default= lambda: str(nanoid.generate(size=12)))

    poll_id: Mapped[int] = mapped_column(ForeignKey('polls.id', ondelete="CASCADE"), index=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String, nullable=False)
    votes: Mapped[int] = mapped_column(Integer, default=0)

    related_poll: Mapped['PollModel'] = relationship(back_populates='options')

class PollModel(Base):
    __tablename__ = "polls"

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(
        String(18),
        primary_key=True, index=True, unique=True,
        default= lambda: str(nanoid.generate(size=12))
    )

    question: Mapped[str] = mapped_column(String, nullable=False)
    options: Mapped[list['PollOption']] = relationship(
        back_populates='related_poll',
        cascade="all, delete-orphan",
        order_by="PollOption.position",
    )

    creator = relationship('UserModel', back_populates='polls')
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    is_indefinite: Mapped[bool] = mapped_column(default=False)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) 

    # Add relationship back to PollHistoryEntry
    polls_history: Mapped[list["PollHistoryEntry"]] = relationship(
        back_populates='related_poll',
        cascade="all, delete-orphan",
        order_by="PollHistoryEntry.timestamp",
    )


class PollHistoryEntry(Base): 
    __tablename__ = "polls_history_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[str] = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"))

    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    related_poll: Mapped["PollModel"] = relationship(back_populates="polls_history")

    __table_args__ = (
        UniqueConstraint("poll_id", "timestamp", name="uix_poll_timestamp"),
    )