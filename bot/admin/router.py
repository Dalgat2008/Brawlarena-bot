from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select

from bot.database import AsyncSessionLocal
from bot.config import settings
from bot.models import Match
from bot.admin.service import AdminService

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👑 Админ-панель\n\n"
        "/matches — все матчи\n"
        "/cancel <id> — отменить матч\n"
        "/winner <match_id> <user_id> — указать победителя"
    )


@router.message(F.text.startswith("/matches"))
async def admin_matches(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with AsyncSessionLocal() as session:
        matches = await session.scalars(select(Match))

    text = "📋 Матчи:\n"
    for m in matches:
        text += f"ID {m.id} | {m.mode} | {m.status}\n"

    await message.answer(text)


@router.message(F.text.startswith("/cancel"))
async def admin_cancel(message: Message):
    if not is_admin(message.from_user.id):
        return

    _, match_id = message.text.split()
    async with AsyncSessionLocal() as session:
        ok = await AdminService.cancel_match(session, int(match_id))

    await message.answer("❌ Матч отменён" if ok else "Ошибка")


@router.message(F.text.startswith("/winner"))
async def admin_winner(message: Message):
    if not is_admin(message.from_user.id):
        return

    _, match_id, user_id = message.text.split()
    async with AsyncSessionLocal() as session:
        ok = await AdminService.set_winner(
            session,
            int(match_id),
            int(user_id),
        )

    await message.answer("🏆 Победитель установлен" if ok else "Ошибка")