import sqlite3


def create_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    full_name TEXT,
                    phone TEXT,
                    language_level TEXT,
                    city TEXT)
                """)
    conn.commit()
    conn.close()
    
def add_user(telegram_id, full_name, phone, language_level, city):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO users(telegram_id, full_name, phone, language_level, city)
                values (?, ?, ?, ?, ?)
                """, (telegram_id, full_name, phone, language_level, city))
    conn.commit()
    conn.close()
    
def get_all_users():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    
    cur.execute("""
                SELECT full_name, phone, language_level, city FROM users
                """)
    users = cur.fetchall()
    
    conn.close()
    return users