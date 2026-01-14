import os 
from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    Integer, Float, Boolean, String, Column, Row,
)
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

dbengine =  create_engine(
    url=str(DATABASE_URL), 
    connect_args={"check_same_thread": False}   # sqlite only
)

Base = declarative_base()

