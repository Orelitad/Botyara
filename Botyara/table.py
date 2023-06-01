import sqlite3

async def conn_start():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS answers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id,
                   chat_id,
                   first_message,
                   second_message,
                   third_message,
                   fourth_message,
                   status)""")
    conn.commit()