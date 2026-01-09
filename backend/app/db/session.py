from sqlalchemy.orm import Session, sessionmaker

from app.db.base import dbengine

session_local = Session(
    bind=dbengine, 
    autocommit=False, 
    autoflush=False
)