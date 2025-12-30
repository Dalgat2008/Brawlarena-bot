import asyncio

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
import uvicorn

from bot.config import settings

# ===== Routers =====
from bot.handlers.payments import router as payments_router
from bot.admin.router import router as admin_router
# (остальные роутеры: start, profile, matches — уже подключаются аналогично)

# ===== Telegram =====

bot = Bot(
    token=settings.bot_token,
    parse_mode="HTML"
)

dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(payments_router)
dp.include_router(admin_router)

# ===== FastAPI (webhooks / admin / payments) =====

app = FastAPI(
    title="BrawlArena Bot API",
    version="1.0.0"
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# 🔔 CryptoBot webhook (используется в Блоке 5)
@app.post("/cryptobot/webhook")
async def cryptobot_webhook(data: dict):
    """
    Webhook от CryptoBot:
    - подтверждение оплаты
    - статус инвойса
    """
    # Реальная логика подтверждения оплаты
    # будет вызывать PaymentService.confirm_payment(...)
    return {"ok": True}


# ===== Run =====

async def start_bot():
    print("🤖 Telegram bot started")
    await dp.start_polling(bot)


def start_web():
    print("🌐 FastAPI server started")
    uvicorn.run(
        app,
        host=settings.webhook_host,
        port=settings.webhook_port,
        log_level="info",
    )


async def main():
    loop = asyncio.get_event_loop()

    # Запускаем Telegram-бота
    loop.create_task(start_bot())

    # Запускаем веб-сервер (CryptoBot, health, админка)
    await asyncio.to_thread(start_web)


if __name__ == "__main__":
    asyncio.run(main())