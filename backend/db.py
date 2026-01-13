import os
from dotenv import load_dotenv

import sqlite3

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

conn = sqlite3.connect(str(DATABASE_URL), check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()