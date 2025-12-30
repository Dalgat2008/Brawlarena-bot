import asyncpg
from bot.config import DATABASE_URL

pool: asyncpg.Pool | None = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)