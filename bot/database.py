import sqlite3

DB_PATH = "brawlarena.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            player_tag TEXT,
            referrer_id INTEGER
        )
        """)

        db.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            telegram_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0
        )
        """)

        db.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER,
            mode TEXT,
            buy_in REAL,
            status TEXT
        )
        """)

        db.execute("""
        CREATE TABLE IF NOT EXISTS match_players (
            match_id INTEGER,
            telegram_id INTEGER,
            PRIMARY KEY (match_id, telegram_id)
        )
        """)

        db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            amount REAL,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)