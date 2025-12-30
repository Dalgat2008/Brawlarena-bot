from aiogram import Router
from aiogram.types import Message
from bot.config import ADMIN_IDS

router = Router()

@router.message(commands=["admin"])
async def admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Админка активна")