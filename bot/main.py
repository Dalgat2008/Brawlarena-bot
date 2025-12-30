from aiogram import Bot, Dispatcher, executor, types

from bot.database import init_db
from bot.users import register_user, get_user
from bot.matches import create_match, join_match
from bot.payments import get_balance, add_balance, hold_balance
from bot.referrals import bind_referral

BOT_TOKEN = "8540060264:AAGun7H2Jxrml9kt4s4su-aQkxmeXF7SX5c"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    args = msg.get_args()
    if args.isdigit():
        bind_referral(msg.from_user.id, int(args))

    await msg.answer(
        "🎮 BrawlArena\n\n"
        "/register TAG\n"
        "/balance\n"
        "/deposit AMOUNT\n"
        "/create_solo AMOUNT\n"
    )


@dp.message_handler(commands=["register"])
async def register(msg: types.Message):
    tag = msg.get_args()
    register_user(msg.from_user.id, msg.from_user.username, tag)
    await msg.answer("✅ Регистрация успешна")


@dp.message_handler(commands=["balance"])
async def balance(msg: types.Message):
    bal = get_balance(msg.from_user.id)
    await msg.answer(f"💰 Баланс: {bal} USDT")


@dp.message_handler(commands=["deposit"])
async def deposit(msg: types.Message):
    amount = float(msg.get_args())
    add_balance(msg.from_user.id, amount)
    await msg.answer(f"✅ Баланс пополнен на {amount}")


@dp.message_handler(commands=["create_solo"])
async def create_solo(msg: types.Message):
    amount = float(msg.get_args())
    if not hold_balance(msg.from_user.id, amount):
        await msg.answer("❌ Недостаточно средств")
        return

    match_id = create_match(msg.from_user.id, "solo")
    await msg.answer(f"✅ Матч создан ID {match_id}")
    

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp)