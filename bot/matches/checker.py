from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.brawl.api import BrawlAPI
from bot.brawl.battles import find_common_battle, determine_winner
from bot.models import Match, MatchStatus, MatchMode, User


class MatchChecker:
    def __init__(self):
        self.api = BrawlAPI()

    async def check_match(
        self,
        session: AsyncSession,
        match_id: int,
    ) -> bool:
        """
        Проверяет матч:
        - собирает battlelog всех игроков
        - ищет общий бой
        - определяет победителя
        """

        result = await session.execute(
            select(Match).where(Match.id == match_id)
        )
        match: Match | None = result.scalar_one_or_none()

        if not match or match.status != MatchStatus.active:
            return False

        players = match.players
        player_tags = [u.player_tag for u in players]

        battlelogs = {}
        for user in players:
            battlelogs[user.player_tag] = await self.api.get_battlelog(
                user.player_tag
            )

        common_battle = find_common_battle(
            battlelogs=battlelogs,
            expected_mode=match.mode,
            player_tags=player_tags,
            started_at=match.started_at,
        )

        if not common_battle:
            return False

        winner_tag = determine_winner(common_battle, match.mode)
        if not winner_tag:
            match.status = MatchStatus.error
            await session.commit()
            return False

        winner = next(
            (u for u in players if u.player_tag == winner_tag), None
        )

        if not winner:
            match.status = MatchStatus.error
            await session.commit()
            return False

        match.winner_id = winner.id
        match.status = MatchStatus.finished
        match.finished_at = datetime.now(tz=timezone.utc)

        await session.commit()
        return True