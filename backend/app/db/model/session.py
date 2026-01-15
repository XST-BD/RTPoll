from datetime import datetime

from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm  import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base

class SessionModel(Base): 

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String, index=True, unique=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.user_id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    

