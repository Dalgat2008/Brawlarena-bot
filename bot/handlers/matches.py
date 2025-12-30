from aiogram import Router
from aiogram.types import Message
from bot.database import pool

router = Router()

@router.message(commands=["create_match"])
async def create_match(message: Message):
    async with pool.acquire() as conn:
        await conn.execute("""
        INSERT INTO matches (mode, creator_id, status)
        VALUES ('duel', $1, 'waiting')
        """, message.from_user.id)

    await message.answer("Матч создан, ждём игроков")