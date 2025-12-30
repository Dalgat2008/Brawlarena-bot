from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models import Match, User, MatchStatus


class AdminService:

    @staticmethod
    async def list_matches(session: AsyncSession):
        return await session.scalars(select(Match))

    @staticmethod
    async def cancel_match(
        session: AsyncSession,
        match_id: int,
    ):
        match = await session.get(Match, match_id)
        if not match:
            return False

        match.status = MatchStatus.canceled
        await session.commit()
        return True

    @staticmethod
    async def set_winner(
        session: AsyncSession,
        match_id: int,
        user_id: int,
    ):
        match = await session.get(Match, match_id)
        if not match:
            return False

        match.winner_id = user_id
        match.status = MatchStatus.finished
        await session.commit()
        return True