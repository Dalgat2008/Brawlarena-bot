from bot.database import get_db


def bind_referral(user_id: int, referrer_id: int):
    if user_id == referrer_id:
        return

    with get_db() as db:
        existing = db.execute(
            "SELECT referrer_id FROM users WHERE telegram_id=?",
            (user_id,)
        ).fetchone()

        if existing and existing[0]:
            return

        db.execute(
            "UPDATE users SET referrer_id=? WHERE telegram_id=?",
            (referrer_id, user_id)
        )


def get_referrer(user_id: int):
    with get_db() as db:
        row = db.execute(
            "SELECT referrer_id FROM users WHERE telegram_id=?",
            (user_id,)
        ).fetchone()
        return row[0] if row else None