from datetime import date, timedelta
from database.streak_db import get_connection

def calculate_level(streak):
    if streak >= 30:
        return "Legend"
    elif streak >= 15:
        return "Warrior"
    elif streak >= 8:
        return "Dedicated"
    elif streak >= 4:
        return "Consistent"
    return "Beginner"


def update_streak():
    today = date.today()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT current_streak, best_streak, last_active_date, grace_used, points FROM user_streak WHERE id=1")
    streak, best, last_date, grace_used, points = cur.fetchone()

    if last_date:
        last_date = date.fromisoformat(last_date)

    # Already counted today
    if last_date == today:
        conn.close()
        return

    # Yesterday → normal increment
    if last_date == today - timedelta(days=1):
        streak += 1
        grace_used = 0

    # Missed one day → grace
    elif last_date == today - timedelta(days=2) and grace_used == 0:
        streak += 1
        grace_used = 1

    # Streak broken
    else:
        streak = 1
        grace_used = 0

    points += 25
    best = max(best, streak)
    level = calculate_level(streak)

    cur.execute("""
        UPDATE user_streak 
        SET current_streak=?, best_streak=?, last_active_date=?, grace_used=?, points=?, level=?
        WHERE id=1
    """, (streak, best, today.isoformat(), grace_used, points, level))

    conn.commit()
    conn.close()


def get_streak_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT current_streak, best_streak, points, level FROM user_streak WHERE id=1")
    data = cur.fetchone()

    conn.close()
    return data