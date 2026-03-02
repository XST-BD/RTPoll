from sqlalchemy.orm import sessionmaker

from app.db.base import dbengine

SessionLocal = sessionmaker(
    bind=dbengine, 
    autocommit=False, 
    autoflush=False
)