import aiohttp
from bot.config import CRYPTOBOT_API_TOKEN

API_URL = "https://pay.crypt.bot/api"

headers = {
    "Crypto-Pay-API-Token": CRYPTOBOT_API_TOKEN
}

async def create_invoice(amount: float):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"{API_URL}/createInvoice", json={
            "asset": "USDT",
            "amount": amount
        }) as r:
            return await r.json()