from aiogram import Router
from aiogram.types import Message
from bot.database import pool

router = Router()

@router.message(commands=["start"])
async def start(message: Message):
    ref = None
    if "ref_" in message.text:
        ref = int(message.text.split("_")[1])

    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO users (tg_id, referrer_id)
        VALUES ($1,$2)
        ON CONFLICT DO NOTHING
        """, message.from_user.id, ref)

    await message.answer("🎮 BrawlArena запущен")