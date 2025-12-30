import asyncio
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
import uvicorn

from bot.config import settings

# ===== Telegram =====

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# handlers будут подключаться позже:
# from bot.handlers import start, profile, matches, payments, admin
# dp.include_router(start.router)
# ...


# ===== FastAPI =====

app = FastAPI(title="BrawlArena Bot API")


@app.get("/health")
async def health():
    return {"status": "ok"}


# webhook для CryptoBot будет добавлен в Блоке 5
# @app.post("/cryptobot/webhook")
# async def cryptobot_webhook(...):


# ===== Run both =====

async def start_bot():
    await dp.start_polling(bot)


def start_web():
    uvicorn.run(
        app,
        host=settings.webhook_host,
        port=settings.webhook_port,
        log_level="info",
    )


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    await asyncio.to_thread(start_web)


if __name__ == "__main__":
    asyncio.run(main())