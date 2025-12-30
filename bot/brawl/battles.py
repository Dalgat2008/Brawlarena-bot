from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from bot.models import MatchMode


def parse_battle_time(battle_time: str) -> datetime:
    # формат: 20240220T123456.000Z
    return datetime.strptime(battle_time, "%Y%m%dT%H%M%S.%fZ").replace(
        tzinfo=timezone.utc
    )


def normalize_player_tag(tag: str) -> str:
    return tag.upper().replace("#", "")


def find_common_battle(
    battlelogs: Dict[str, List[dict]],
    expected_mode: MatchMode,
    player_tags: List[str],
    started_at: datetime,
    time_window_sec: int = 300,
) -> Optional[dict]:
    """
    Ищем ОДИН И ТОТ ЖЕ бой у всех игроков:
    - совпадает режим
    - совпадает набор игроков
    - время рядом со started_at
    """

    normalized_tags = {normalize_player_tag(t) for t in player_tags}

    for tag, battles in battlelogs.items():
        for battle in battles:
            battle_time = parse_battle_time(battle["battleTime"])

            if abs((battle_time - started_at).total_seconds()) > time_window_sec:
                continue

            event_mode = battle.get("event", {}).get("mode")
            if expected_mode == MatchMode.solo and event_mode != "soloShowdown":
                continue
            if expected_mode == MatchMode.duel and event_mode != "duels":
                continue

            players = battle["battle"].get("players") or []
            battle_tags = {
                normalize_player_tag(p["tag"]) for p in players if "tag" in p
            }

            if battle_tags == normalized_tags:
                return battle

    return None


def determine_winner(
    battle: dict,
    mode: MatchMode,
) -> Optional[str]:
    """
    Возвращает player_tag победителя
    """

    players = battle["battle"].get("players") or []

    if mode == MatchMode.solo:
        # В Solo 1 место = победитель
        for p in players:
            if p.get("rank") == 1:
                return p["tag"]

    if mode == MatchMode.duel:
        # В Duel winner указан напрямую
        for p in players:
            if p.get("result") == "victory":
                return p["tag"]

    return None