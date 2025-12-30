import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🎮 *Brawlarena*\n\n"
        "Бот для кастомных матчей Brawl Stars.\n\n"
        "Доступно:\n"
        "• Solo (2–10 игроков)\n"
        "• Duel (1v1)\n\n"
        "Скоро:\n"
        "• Регистрация\n"
        "• Матчи\n"
        "• Проверка результатов",
        parse_mode="Markdown"
    )


async def main():
    logging.info("🚀 Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())