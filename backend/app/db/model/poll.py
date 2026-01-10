from typing import List

from sqlalchemy import (
    Integer, Float, Boolean, String, Column, Row, JSON, ForeignKey
)
from sqlalchemy.orm import relationship

from app.db.base import Base

class PollModel(Base):

    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    creator_name = Column(String, nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    expirey = Column(Integer, nullable=False)

    # Relationship with user
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("UserModel", back_populates="polls")

