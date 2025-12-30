from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models import Match, MatchMode, MatchStatus, User


class MatchService:
    @staticmethod
    async def create_match(
        session: AsyncSession,
        creator: User,
        mode: MatchMode,
        max_players: int,
    ) -> Match:
        match = Match(
            mode=mode,
            max_players=max_players,
            status=MatchStatus.waiting,
        )
        session.add(match)
        await session.flush()

        match.players.append(creator)
        await session.commit()
        return match

    @staticmethod
    async def join_match(
        session: AsyncSession,
        match: Match,
        user: User,
    ) -> bool:
        if match.status != MatchStatus.waiting:
            return False

        if user in match.players:
            return False

        if len(match.players) >= match.max_players:
            return False

        match.players.append(user)

        if len(match.players) == match.max_players:
            match.status = MatchStatus.active
            match.started_at = datetime.now(tz=timezone.utc)

        await session.commit()
        return True

    @staticmethod
    async def set_lobby_code(
        session: AsyncSession,
        match: Match,
        lobby_code: str,
        user: User,
    ) -> bool:
        if match.status != MatchStatus.active:
            return False

        if match.players[0].id != user.id:
            return False  # только создатель

        match.lobby_code = lobby_code
        await session.commit()
        return True

    @staticmethod
    async def get_active_matches(
        session: AsyncSession,
    ) -> list[Match]:
        result = await session.execute(
            select(Match).where(Match.status == MatchStatus.waiting)
        )
        return result.scalars().all()