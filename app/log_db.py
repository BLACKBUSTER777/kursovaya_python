# app/log_db.py
"""
Простой модуль для ведения логов в базе данных SQLite.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "app_logs.db"


def init_db():
    """Создаёт таблицу логов, если её ещё нет."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_log(action: str, result: str):
    """Добавляет новую запись в таблицу логов."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (timestamp, action, result) VALUES (?, ?, ?)",
        (datetime.now().isoformat(timespec="seconds"), action, result[:500])
    )
    conn.commit()
    conn.close()
