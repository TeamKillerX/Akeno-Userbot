import sqlite3

conn = sqlite3.connect('bot_prefix.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prefixes (
        user_id INTEGER PRIMARY KEY,
        prefix TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

async def set_prefix_in_db(user_id: int, prefix: str):
    conn = sqlite3.connect('bot_prefix.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO prefixes (user_id, prefix)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET prefix=excluded.prefix
    ''', (user_id, prefix))

    conn.commit()
    conn.close()

async def get_prefix(user_id: int):
    conn = sqlite3.connect('bot_prefix.db')
    cursor = conn.cursor()

    cursor.execute('SELECT prefix FROM prefixes WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None
