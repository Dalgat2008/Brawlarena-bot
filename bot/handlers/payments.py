from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from bot.database import AsyncSessionLocal
from bot.models import User
from bot.payments.service import PaymentService

router = Router()


@router.message(F.text == "/deposit")
async def deposit(message: Message):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        url = await PaymentService.create_deposit(
            session=session,
            user=user,
            amount=10,
        )

    await message.answer(
        f"💸 Пополнение баланса\nОплати по ссылке:\n{url}"
    )