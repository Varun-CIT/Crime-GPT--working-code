"""
database.py — Unified SQLite setup for CrimeGPT Unified Architecture.
"""

import sqlite3
from contextlib import contextmanager
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager
def db_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db_cursor() as cur:
        # Users Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('citizen', 'officer'))
            )
        """)

        # FIR Records Table (Unified)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fir_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT UNIQUE NOT NULL,
                citizen_username TEXT NOT NULL,
                citizen_phone TEXT,
                officer_username TEXT,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                audio_file TEXT,
                attachments TEXT,
                category TEXT,
                suggested_section TEXT,
                cognizable INTEGER,
                fir_json TEXT, 
                status TEXT DEFAULT 'Submitted',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Append-only hash-chained audit log
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                actor_username TEXT NOT NULL,
                actor_role TEXT NOT NULL,
                action TEXT NOT NULL,
                data_snapshot TEXT NOT NULL,
                timestamp TEXT DEFAULT (datetime('now')),
                prev_hash TEXT NOT NULL,
                record_hash TEXT NOT NULL,
                FOREIGN KEY (case_id) REFERENCES fir_records(case_id)
            )
        """)
    print(f"Database initialized at {DB_PATH}")

def get_case(case_id: str):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM fir_records WHERE case_id = ?", (case_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def get_all_cases():
    with db_cursor() as cur:
        cur.execute("SELECT * FROM fir_records ORDER BY created_at DESC")
        return [dict(row) for row in cur.fetchall()]

if __name__ == "__main__":
    init_db()
