from bot.database import pool

async def reward_referrers(match_id: int, commission: float):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT u.referrer_id
        FROM match_players mp
        JOIN users u ON u.tg_id = mp.tg_id
        WHERE mp.match_id=$1 AND u.referrer_id IS NOT NULL
        """, match_id)

        if not rows:
            return

        reward = commission * 0.3 / len(rows)
        for r in rows:
            await conn.execute("""
            UPDATE users SET balance = balance + $1
            WHERE tg_id=$2
            """, reward, r["referrer_id"])