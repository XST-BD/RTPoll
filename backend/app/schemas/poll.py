# from pydantic import BaseModel, Field
# from typing import List

# class PollCreate(BaseModel):
#     question: str = Field(..., min_length=1)    # must be non-empty string
#     options: list[str] = Field(..., min_length=2, max_length=10)
#     expires_at: int

# class PollView(BaseModel):
#     id: int
#     question: str
#     expires_at: int
#     options: List[str]

#     class Config:
#         from_attributes = True   # REQUIRED for SQLAlchemy