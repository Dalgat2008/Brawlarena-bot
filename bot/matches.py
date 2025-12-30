from bot.database import get_db


def create_match(owner_id: int, mode: str):
    with get_db() as db:
        db.execute(
            """
            INSERT INTO matches (owner_id, mode, is_active)
            VALUES (?, ?, 1)
            """,
            (owner_id, mode)
        )
        db.commit()


def get_active_match():
    with get_db() as db:
        cur = db.execute(
            "SELECT id, owner_id, mode FROM matches WHERE is_active = 1 LIMIT 1"
        )
        return cur.fetchone()


def join_match(match_id: int, user_id: int):
    with get_db() as db:
        db.execute(
            "INSERT INTO match_players (match_id, user_id) VALUES (?, ?)",
            (match_id, user_id)
        )
        db.commit()


def leave_match(match_id: int, user_id: int):
    with get_db() as db:
        db.execute(
            "DELETE FROM match_players WHERE match_id = ? AND user_id = ?",
            (match_id, user_id)
        )
        db.commit()


def get_players(match_id: int):
    with get_db() as db:
        cur = db.execute(
            """
            SELECT u.telegram_id, u.nickname
            FROM users u
            JOIN match_players mp ON u.telegram_id = mp.user_id
            WHERE mp.match_id = ?
            """,
            (match_id,)
        )
        return cur.fetchall()