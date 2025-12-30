from bot.database import get_db
from datetime import datetime

MAX_PLAYERS = {
    "solo": 10,
    "duel": 2
}


def mark_match_finished(match_id: int):
    with get_db() as db:
        db.execute(
            "UPDATE matches SET status='finished' WHERE id=?",
            (match_id,)
        )


def get_active_matches():
    with get_db() as db:
        return db.execute(
            """
            SELECT id, mode, buy_in
            FROM matches
            WHERE status='in_game'
            """
        ).fetchall()


def get_match_players_full(match_id: int):
    with get_db() as db:
        return db.execute(
            """
            SELECT u.telegram_id, u.player_tag, u.referrer_id
            FROM match_players mp
            JOIN users u ON u.telegram_id = mp.telegram_id
            WHERE mp.match_id=?
            """,
            (match_id,)
        ).fetchall()


def get_match_start_time(match_id: int):
    with get_db() as db:
        row = db.execute(
            "SELECT created_at FROM matches WHERE id=?",
            (match_id,)
        ).fetchone()
        return datetime.fromisoformat(row[0])