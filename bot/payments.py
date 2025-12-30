from bot.database import get_db

PLATFORM_FEE_PERCENT = 10
REFERRAL_PERCENT_FROM_FEE = 30


def get_balance(user_id: int) -> float:
    with get_db() as db:
        row = db.execute(
            "SELECT balance FROM balances WHERE telegram_id=?",
            (user_id,)
        ).fetchone()
        return row[0] if row else 0.0


def add_balance(user_id: int, amount: float):
    with get_db() as db:
        db.execute(
            "INSERT OR IGNORE INTO balances (telegram_id, balance) VALUES (?, 0)",
            (user_id,)
        )
        db.execute(
            "UPDATE balances SET balance = balance + ? WHERE telegram_id=?",
            (amount, user_id)
        )
        db.execute(
            "INSERT INTO transactions (telegram_id, amount, type) VALUES (?, ?, 'deposit')",
            (user_id, amount)
        )


def hold_balance(user_id: int, amount: float) -> bool:
    with get_db() as db:
        bal = get_balance(user_id)
        if bal < amount:
            return False

        db.execute(
            "UPDATE balances SET balance = balance - ? WHERE telegram_id=?",
            (amount, user_id)
        )
        db.execute(
            "INSERT INTO transactions (telegram_id, amount, type) VALUES (?, ?, 'hold')",
            (user_id, -amount)
        )
    return True


def distribute_prize(winner_id: int, total_bank: float, referrer_id: int | None):
    fee = total_bank * PLATFORM_FEE_PERCENT / 100
    prize = total_bank - fee

    with get_db() as db:
        db.execute(
            "UPDATE balances SET balance = balance + ? WHERE telegram_id=?",
            (prize, winner_id)
        )
        db.execute(
            "INSERT INTO transactions (telegram_id, amount, type) VALUES (?, ?, 'win')",
            (winner_id, prize)
        )

        if referrer_id:
            ref_reward = fee * REFERRAL_PERCENT_FROM_FEE / 100
            db.execute(
                "UPDATE balances SET balance = balance + ? WHERE telegram_id=?",
                (ref_reward, referrer_id)
            )