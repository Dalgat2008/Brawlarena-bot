from aiogram import Router
from aiogram.types import Message
from bot.database import pool

router = Router()

@router.message(commands=["profile"])
async def profile(message: Message):
    async with pool.acquire() as conn:
        u = await conn.fetchrow("SELECT * FROM users WHERE tg_id=$1", message.from_user.id)

    await message.answer(
        f"👤 Профиль\n"
        f"PlayerTag: {u['player_tag']}\n"
        f"Wins: {u['wins']} | Losses: {u['losses']}"
    )