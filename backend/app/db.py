import sqlite3
import logging
from datetime import datetime, UTC
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent.parent / "data" / "nexus.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    logger.info("Initializing database...")
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS metric_snapshots (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                source      TEXT NOT NULL,
                captured_at TEXT NOT NULL,
                data        TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS daily_briefs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT NOT NULL,
                brief       TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_snapshots_source_date
                ON metric_snapshots(source, captured_at);
        """)
    logger.info("Database ready.")