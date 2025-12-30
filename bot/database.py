import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import BOT_TOKEN
from bot.database import init_db, get_db


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ---------- STATES ----------
class Register(StatesGroup):
    nickname = State()
    player_tag = State()


# ---------- START ----------
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    db = get_db()
    user = db.execute(
        "SELECT telegram_id FROM users WHERE telegram_id = ?",
        (message.from_user.id,)
    ).fetchone()
    db.close()

    if user:
        await message.answer("✅ Ты уже зарегистрирован.")
        return

    await message.answer("👋 Добро пожаловать!\n\nВведи никнейм:")
    await state.set_state(Register.nickname)


# ---------- NICKNAME ----------
@dp.message(Register.nickname)
async def set_nickname(message: Message, state: FSMContext):
    nickname = message.text.strip()

    if len(nickname) < 3:
        await message.answer("❌ Ник слишком короткий. Попробуй ещё раз:")
        return

    await state.update_data(nickname=nickname)
    await message.answer("🎮 Теперь введи Player Tag Brawl Stars (пример: #ABC123):")
    await state.set_state(Register.player_tag)


# ---------- PLAYER TAG ----------
@dp.message(Register.player_tag)
async def set_player_tag(message: Message, state: FSMContext):
    tag = message.text.strip().upper()

    if not tag.startswith("#") or len(tag) < 5:
        await message.answer("❌ Неверный Player Tag. Пример: #ABC123")
        return

    data = await state.get_data()

    db = get_db()
    db.execute(
        "INSERT INTO users (telegram_id, username, nickname, player_tag) VALUES (?, ?, ?, ?)",
        (
            message.from_user.id,
            message.from_user.username,
            data["nickname"],
            tag
        )
    )
    db.commit()
    db.close()

    await state.clear()
    await message.answer(
        "✅ Регистрация завершена!\n\n"
        f"Ник: {data['nickname']}\n"
        f"Player Tag: {tag}"
    )


# ---------- RUN ----------
async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())