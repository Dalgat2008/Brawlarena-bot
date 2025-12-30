import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database import init_db
from bot.handlers import start, profile, matches, payments, admin

async def main():
    await init_db()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(matches.router)
    dp.include_router(payments.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())