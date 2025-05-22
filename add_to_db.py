import sqlite3

conn = sqlite3.connect('db/users_.db')
cursor = conn.cursor()


cursor.execute("""
        ALTER TABLE users
        ADD COLUMN history_count INTEGER DEFAULT 0 CHECK(history_count >= 0 AND history_count <= 20)
    """)

conn.commit()
conn.close()