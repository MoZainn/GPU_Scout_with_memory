"""
Persistent, cross-session memory for GPU Scout.

The in-memory `st.session_state.history` (see app.py) only lives for as
long as the browser tab is open — it resets on refresh. This module adds
a second, durable layer: every turn is written to a local SQLite file
keyed by a user_id, so a returning user's history can be reloaded even
after closing the app entirely.

SQLite (not Postgres/Redis) is a deliberate choice here: this is a
single-machine portfolio project, not a multi-server production service,
so a single flat file that needs zero setup is the right-sized tool.
"""

import sqlite3
import time

import config


def _connect():
    conn = sqlite3.connect(config.MEMORY_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            question TEXT NOT NULL,
            category TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at REAL NOT NULL
        )
        """
    )
    return conn


def save_turn(user_id, question, category, answer):
    """Persist a single Q&A turn for this user."""
    conn = _connect()
    with conn:
        conn.execute(
            """
            INSERT INTO conversations (user_id, question, category, answer, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, question, category, answer, time.time()),
        )
    conn.close()


def load_history(user_id, limit=config.MEMORY_DISPLAY_LIMIT):
    """
    Return this user's most recent turns, oldest first, as a list of
    {"question", "category", "answer"} dicts — the same shape
    st.session_state.history already uses, so it can be dropped straight in.
    """
    conn = _connect()
    rows = conn.execute(
        """
        SELECT question, category, answer FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()
    conn.close()

    rows.reverse()
    return [
        {"question": q, "category": c, "answer": a}
        for q, c, a in rows
    ]


def clear_history(user_id):
    """Wipe this user's persisted history (used by the 'Clear conversation' button)."""
    conn = _connect()
    with conn:
        conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
    conn.close()
