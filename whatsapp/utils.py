import json
import sqlite3
from contextlib import contextmanager

DB_PATH = "whatsapp/chats.db"  # not session.db, that one belongs to neonize


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                user_id    TEXT PRIMARY KEY,
                history    TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def load_history(user_id: str) -> list[dict] | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT history FROM sessions WHERE user_id = ?", (user_id,)
        ).fetchone()
    return json.loads(row[0]) if row else None


def save_history(user_id: str, history: list[dict]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO sessions (user_id, history)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                history = excluded.history,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, json.dumps(history)),
        )


def delete_history(user_id: str) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))