from aiogram import Bot, Dispatcher, executor, types
import asyncio

from bot.database import init_db
from bot.matches import (
    get_active_matches,
    get_match_players_full,
    get_match_start_time,
    mark_match_finished
)
from bot.brawl_api import find_common_battle
from bot.payments import distribute_prize
from bot.referrals import get_referrer

BOT_TOKEN = "8540060264:AAGun7H2Jxrml9kt4s4su-aQkxmeXF7SX5c"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def check_matches_loop():
    while True:
        matches = get_active_matches()

        for match_id, mode, buy_in in matches:
            players = get_match_players_full(match_id)
            tags = [p[1] for p in players]
            start_time = get_match_start_time(match_id)

            battle = find_common_battle(tags, start_time)
            if not battle:
                continue

            if mode == "solo":
                winner_tag = battle["battle"]["rankings"][0]["tag"]
            else:
                winner_tag = battle["battle"]["result"]["winner"]["tag"]

            winner = next(p for p in players if p[1] == winner_tag)

            total_bank = buy_in * len(players)
            referrer = get_referrer(winner[0])

            distribute_prize(
                winner_id=winner[0],
                total_bank=total_bank,
                referrer_id=referrer
            )

            mark_match_finished(match_id)

            for p in players:
                await bot.send_message(
                    p[0],
                    f"🏁 Матч #{match_id} завершён\n"
                    f"Победитель: {winner_tag}"
                )

        await asyncio.sleep(60)


if name == "__main__":
    init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(check_matches_loop())
    executor.start_polling(dp)