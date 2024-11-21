import sqlite3
from datetime import datetime, timedelta

# 初始化数据库
def init_db():
    conn = sqlite3.connect("genshin_boss_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boss_history (
            boss_name TEXT,
            draw_date DATE
        )
    """)
    conn.commit()
    conn.close()

# 添加抽取记录
def add_draw(boss_name):
    conn = sqlite3.connect("genshin_boss_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO boss_history (boss_name, draw_date) VALUES (?, ?)", (boss_name, datetime.now().date()))
    conn.commit()
    conn.close()

# 查询一周内的抽取记录
def get_recent_draws():
    conn = sqlite3.connect("genshin_boss_history.db")
    cursor = conn.cursor()
    one_week_ago = datetime.now().date() - timedelta(days=7)
    cursor.execute("SELECT boss_name, COUNT(*) FROM boss_history WHERE draw_date >= ? GROUP BY boss_name", (one_week_ago,))
    result = cursor.fetchall()
    conn.close()
    return dict(result)
