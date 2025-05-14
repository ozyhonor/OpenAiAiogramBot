import sqlite3

conn = sqlite3.connect('db/users_.db')
cursor = conn.cursor()

# Добавляем history_count (если его нет)
try:
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN history_count INTEGER DEFAULT 1 CHECK(history_count >= 0 AND history_count <= 10)
    """)
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Столбец history_count уже существует.")
    else:
        raise

# Добавляем history_message (если его нет)
try:
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN history_message TEXT
    """)
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Столбец history_message уже существует.")
    else:
        raise

conn.commit()
conn.close()