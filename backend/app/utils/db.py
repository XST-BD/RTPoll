import sqlite3

from app.db.base import dbengine

db_path = str(dbengine.url.database)

def delete_hard(table_name, condition, params):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(sql, params)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Deleted from {table_name} where {condition} = {params}\nFor email migration")