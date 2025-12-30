import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --------------------
# ВРЕМЕННОЕ ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ
# потом заменим на БД
# --------------------
users = {}


def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="👤 Профиль"))
    kb.add(KeyboardButton(text="🎮 Найти матч"))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


# --------------------
# /start — регистрация
# --------------------
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            "id": user_id,
            "username": message.from_user.username,
            "registered_at": datetime.now(),
            "games": 0,
            "wins": 0,
            "balance": 0
        }

    await message.answer(
        "🔥 Добро пожаловать в *Brawlarena!*\n\n"
        "Здесь ты можешь участвовать в кастомных матчах Brawl Stars.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


# --------------------
# Профиль игрока
# --------------------
@dp.message(lambda m: m.text == "👤 Профиль")
async def profile_handler(message: types.Message):
    user = users.get(message.from_user.id)

    if not user:
        await message.answer("❌ Профиль не найден. Напиши /start")
        return

    text = (
        f"👤 *Твой профиль*\n\n"
        f"🆔 ID: `{user['id']}`\n"
        f"👤 Username: @{user['username']}\n"
        f"🎮 Игр сыграно: {user['games']}\n"
        f"🏆 Побед: {user['wins']}\n"
        f"💰 Баланс: {user['balance']} ₽"
    )

    await message.answer(text, parse_mode="Markdown")


# --------------------
# Заглушка под матчи
# --------------------
@dp.message(lambda m: m.text == "🎮 Найти матч")
async def match_stub(message: types.Message):
    await message.answer(
        "⏳ Поиск матча скоро будет доступен.\n"
        "Этот раздел мы сделаем в *Блоке 3*."
    )


# --------------------
# Запуск
# --------------------
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())