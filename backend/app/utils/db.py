import os
from dotenv import load_dotenv
import sqlite3
import psycopg2

from app.db.base import dbengine

load_dotenv()
db_path = str(dbengine.url.database)

DBNAME = os.getenv("POSTGRES_DB", "POSTGRES_DB")
DBUSER = os.getenv("POSTGRES_USER", "POSTGRES_USER")
DBPASS = os.getenv("POSTGRES_PASSWORD", "POSTGRES_PASSWORD")

def delete_hard(table_name, condition, params):
    # conn = sqlite3.connect(db_path)
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=DBUSER,
        password=DBPASS,
        host="rtpoll_psql",
        port="5432"
    )
    cursor = conn.cursor()

    sql = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(sql, params)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Deleted from {table_name} where {condition} = {params}\nFor email migration")