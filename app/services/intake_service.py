import os
import sqlite3
from datetime import datetime, date
from typing import List, Tuple, Optional


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _data_dir() -> str:
    d = os.path.join(_project_root(), "storage", "data")
    os.makedirs(d, exist_ok=True)
    return d


def db_path() -> str:
    return os.path.join(_data_dir(), "intake.db")


def init_db() -> None:
    con = sqlite3.connect(db_path())
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                amount_ml INTEGER NOT NULL
            )
            """
        )
        con.commit()
    finally:
        con.close()


def add_intake(amount_ml: int, ts: Optional[datetime] = None) -> None:
    if ts is None:
        ts = datetime.now()
    init_db()
    con = sqlite3.connect(db_path())
    try:
        con.execute("INSERT INTO intake (ts, amount_ml) VALUES (?, ?)", (ts.isoformat(timespec="seconds"), int(amount_ml)))
        con.commit()
    finally:
        con.close()


def get_today_total() -> int:
    init_db()
    con = sqlite3.connect(db_path())
    try:
        today = date.today().isoformat()  # YYYY-MM-DD
        cur = con.execute(
            "SELECT COALESCE(SUM(amount_ml), 0) FROM intake WHERE substr(ts,1,10)=?",
            (today,),
        )
        row = cur.fetchone()
        return int(row[0] or 0)
    finally:
        con.close()


def get_recent(limit: int = 20) -> List[Tuple[str, int]]:
    init_db()
    con = sqlite3.connect(db_path())
    try:
        cur = con.execute(
            "SELECT ts, amount_ml FROM intake ORDER BY ts DESC LIMIT ?",
            (int(limit),),
        )
        return [(r[0], int(r[1])) for r in cur.fetchall()]
    finally:
        con.close()
