import os
import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional, Dict


def _project_root() -> str:
    # app/services -> app -> repo root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _data_dir() -> str:
    d = os.path.join(_project_root(), "storage", "data")
    os.makedirs(d, exist_ok=True)
    return d


def _get_db_path() -> str:
    """Función pública para obtener la ruta de la BD (usada por profile_service)."""
    return os.path.join(_data_dir(), "intake.db")


def db_path() -> str:
    return _get_db_path()


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
        con.execute(
            "INSERT INTO intake (ts, amount_ml) VALUES (?, ?)", (ts.isoformat(timespec="seconds"), int(amount_ml))
        )
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


def get_between_dates(start: date, end: date) -> List[Tuple[str, int]]:
    """Devuelve intakes entre fechas inclusive, ordenados desc por ts.
    start/end son objetos date (local)."""
    init_db()
    con = sqlite3.connect(db_path())
    try:
        cur = con.execute(
            """
            SELECT ts, amount_ml
            FROM intake
            WHERE substr(ts,1,10) BETWEEN ? AND ?
            ORDER BY ts DESC
            """,
            (start.isoformat(), end.isoformat()),
        )
        return [(r[0], int(r[1])) for r in cur.fetchall()]
    finally:
        con.close()


def get_daily_totals(days: int = 7) -> List[Tuple[str, int]]:
    """Totales por día para los últimos N días (incluye hoy). Orden ascendente por fecha."""
    init_db()
    con = sqlite3.connect(db_path())
    try:
        start = (date.today() - timedelta(days=days - 1)).isoformat()
        end = date.today().isoformat()
        cur = con.execute(
            """
            SELECT substr(ts,1,10) as d, COALESCE(SUM(amount_ml),0) as total
            FROM intake
            WHERE d BETWEEN ? AND ?
            GROUP BY d
            ORDER BY d ASC
            """,
            (start, end),
        )
        return [(r[0], int(r[1])) for r in cur.fetchall()]
    finally:
        con.close()


def delete_last_intake() -> Optional[Tuple[str, int]]:
    """Elimina la última ingesta (por ts más reciente). Devuelve (ts, amount) si existía."""
    init_db()
    con = sqlite3.connect(db_path())
    try:
        cur = con.execute("SELECT id, ts, amount_ml FROM intake ORDER BY ts DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            return None
        _id, ts_val, amount = row
        con.execute("DELETE FROM intake WHERE id=?", (_id,))
        con.commit()
        return (ts_val, int(amount))
    finally:
        con.close()
