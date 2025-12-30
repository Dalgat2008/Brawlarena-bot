import aiohttp
from typing import Any, Dict, List

from bot.config import settings


BRAWL_API_BASE = "https://api.brawlstars.com/v1"


class BrawlAPIError(Exception):
    pass


class BrawlAPI:
    def __init__(self):
        self.headers = {
            # Supercell token НЕ начинается с Bearer — добавляем тут
            "Authorization": f"Bearer {settings.brawl_api_token}",
            "Accept": "application/json",
        }

    async def _get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{BRAWL_API_BASE}{endpoint}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise BrawlAPIError(f"Brawl API error {resp.status}: {text}")
                return await resp.json()

    async def get_player(self, player_tag: str) -> Dict[str, Any]:
        tag = player_tag.replace("#", "%23")
        return await self._get(f"/players/{tag}")

    async def get_battlelog(self, player_tag: str) -> List[Dict[str, Any]]:
        tag = player_tag.replace("#", "%23")
        data = await self._get(f"/players/{tag}/battlelog")
        return data.get("items", [])