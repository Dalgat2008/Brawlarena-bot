from bot.brawl_api import get_battlelog

async def check_match(player_tags: list[str]):
    logs = [await get_battlelog(t) for t in player_tags]
    # упрощённо: берем последний матч
    return logs[0]["items"][0]