import aiohttp
from bot.config import BRAWL_API_TOKEN

BASE_URL = "https://api.brawlstars.com/v1"

headers = {
    "Authorization": f"Bearer {BRAWL_API_TOKEN}"
}

async def get_player(player_tag: str):
    tag = player_tag.replace("#", "%23")
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{BASE_URL}/players/{tag}") as r:
            return await r.json()

async def get_battlelog(player_tag: str):
    tag = player_tag.replace("#", "%23")
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{BASE_URL}/players/{tag}/battlelog") as r:
            return await r.json()