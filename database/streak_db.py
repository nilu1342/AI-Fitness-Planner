import sqlite3
from datetime import date

DB_NAME = "database/streak.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_streak_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_streak (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        current_streak INTEGER DEFAULT 0,
        best_streak INTEGER DEFAULT 0,
        last_active_date TEXT,
        grace_used INTEGER DEFAULT 0,
        points INTEGER DEFAULT 0,
        level TEXT DEFAULT 'Beginner'
    )
    """)

    # Insert default row if empty
    cur.execute("SELECT COUNT(*) FROM user_streak")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO user_streak 
        (current_streak, best_streak, last_active_date, grace_used, points, level)
        VALUES (0, 0, NULL, 0, 0, 'Beginner')
        """)

    conn.commit()
    conn.close()