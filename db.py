import os
import sqlite3

def create_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL
    )
    ''')

    # index
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users (username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id)')

    for dirpath, _, filenames in os.walk('chars'):
        for filename in filenames:
            if filename == 'data.txt':
                file_path = os.path.join(dirpath, filename)
                print(f"processing {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        username, user_id = line.strip().split(',')
                        cursor.execute("INSERT OR IGNORE INTO users (username, user_id) VALUES (?, ?)", (username, int(user_id)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db("sui_usernames.db")