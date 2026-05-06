import os 

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL2', 'DATABASE_URL2')
dbengine =  create_engine(
    url=DATABASE_URL,
    # connect_args={"check_same_thread": False}   # sqlite only
)

Base = declarative_base()

