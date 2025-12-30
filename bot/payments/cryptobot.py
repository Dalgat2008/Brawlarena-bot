import aiohttp

CRYPTOBOT_API = "https://pay.crypt.bot/api"


class CryptoBotClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Crypto-Pay-API-Token": token
        }

    async def create_invoice(
        self,
        amount: float,
        asset: str = "USDT",
        description: str = "BrawlArena deposit",
    ):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                f"{CRYPTOBOT_API}/createInvoice",
                json={
                    "amount": amount,
                    "asset": asset,
                    "description": description,
                }
            ) as resp:
                data = await resp.json()
                return data["result"]

    async def transfer(
        self,
        user_id: int,
        amount: float,
        asset: str = "USDT",
    ):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                f"{CRYPTOBOT_API}/transfer",
                json={
                    "user_id": user_id,
                    "amount": amount,
                    "asset": asset,
                }
            ) as resp:
                return await resp.json()