import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "earnings.db")


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS pushed_earnings (
            symbol TEXT NOT NULL,
            date   TEXT NOT NULL,
            PRIMARY KEY (symbol, date)
        )
    """)
    con.commit()
    con.close()


def already_pushed(symbol: str, date: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        "SELECT 1 FROM pushed_earnings WHERE symbol=? AND date=?", (symbol, date)
    )
    found = cur.fetchone() is not None
    con.close()
    return found


def mark_pushed(symbol: str, date: str):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT OR IGNORE INTO pushed_earnings (symbol, date) VALUES (?,?)",
        (symbol, date),
    )
    con.commit()
    con.close()
