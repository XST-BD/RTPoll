# from typing import List

# from sqlalchemy import (
#     Integer, Float, Boolean, String, Column, Row, JSON, ForeignKey, DateTime
# )
# from sqlalchemy.orm import relationship

# from app.db.base import Base

# class PollModel(Base):

#     __tablename__ = "polls"

#     id = Column(Integer, primary_key=True, index=True)
#     question = Column(String, nullable=False)
#     options = Column(JSON, nullable=False)

#     # Relationship with user
#     creator = relationship("UserModel", back_populates="polls")
#     creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     creator_name = Column(String, nullable=False)

#     slug = Column(String, unique=True, index=True)
#     expires_at = Column(DateTime, nullable=False)

