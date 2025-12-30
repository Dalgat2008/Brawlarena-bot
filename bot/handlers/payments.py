from aiogram import Router
from aiogram.types import Message
from bot.crypto_pay import create_invoice

router = Router()

@router.message(commands=["deposit"])
async def deposit(message: Message):
    invoice = await create_invoice(5)
    await message.answer(invoice["result"]["pay_url"])