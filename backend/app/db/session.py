from sqlalchemy.orm import Session

from app.db.base import dbengine

session_local = Session(
    bind=dbengine, 
    autocommit=False, 
    autoflush=False
)