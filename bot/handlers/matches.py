from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from bot.database import AsyncSessionLocal
from bot.models import Match, MatchMode, User
from bot.matches.service import MatchService
from bot.keyboards.inline import choose_mode, join_match

router = Router()


@router.message(F.text == "/matches")
async def matches_menu(message: Message):
    await message.answer(
        "🎮 Матчи\nВыбери действие:",
        reply_markup=choose_mode(),
    )


@router.callback_query(F.data.startswith("mode_"))
async def create_match(callback: CallbackQuery):
    mode = MatchMode.solo if callback.data == "mode_solo" else MatchMode.duel
    max_players = 10 if mode == MatchMode.solo else 2

    async with AsyncSessionLocal() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == callback.from_user.id)
        )

        match = await MatchService.create_match(
            session=session,
            creator=user,
            mode=mode,
            max_players=max_players,
        )

    await callback.message.answer(
        f"✅ Матч создан!\n"
        f"ID: {match.id}\n"
        f"Режим: {mode.value}\n"
        f"Игроков: 1/{max_players}",
        reply_markup=join_match(match.id),
    )


@router.callback_query(F.data.startswith("join_"))
async def join(callback: CallbackQuery):
    match_id = int(callback.data.split("_")[1])

    async with AsyncSessionLocal() as session:
        match = await session.get(Match, match_id)
        user = await session.scalar(
            select(User).where(User.telegram_id == callback.from_user.id)
        )

        success = await MatchService.join_match(session, match, user)

    if not success:
        await callback.answer("❌ Не удалось войти", show_alert=True)
        return

    await callback.message.answer(
        f"➕ Игрок вошёл\n"
        f"Матч #{match.id}\n"
        f"Участников: {len(match.players)}/{match.max_players}"
    )


@router.message(F.text.startswith("/lobby "))
async def lobby_code(message: Message):
    code = message.text.replace("/lobby ", "").strip()

    async with AsyncSessionLocal() as session:
        match = await session.scalar(
            select(Match)
            .where(Match.status == "active")
            .order_by(Match.created_at.desc())
        )

        user = await session.scalar(
            select(User).where(User.telegram_id == message.from_user.id)
        )

        ok = await MatchService.set_lobby_code(
            session=session,
            match=match,
            lobby_code=code,
            user=user,
        )

    if not ok:
        await message.answer("❌ Ты не можешь установить код")
        return

    for p in match.players:
        await message.bot.send_message(
            p.telegram_id,
            f"🎮 Матч #{match.id}\nКод комнаты:\n{code}",
        )