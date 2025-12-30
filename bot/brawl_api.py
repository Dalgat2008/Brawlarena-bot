import requests
from datetime import datetime, timedelta

BRAWL_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImJlYTIzOGRmLTRhM2UtNDE1Yi05MWNlLWVjMWYxNGJjZDNlOCIsImlhdCI6MTc2NzA4Mjc2NSwic3ViIjoiZGV2ZWxvcGVyLzdjY2UyYTQwLTEwYjgtMDg4MS0yMDdjLTBkN2JmNDI0NDQ1MCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTA5LjE5Ni4xMDEuMTQ0Il0sInR5cGUiOiJjbGllbnQifV19.2WDjcYLyWJ_Bg7MqqiHWQLXxkZotHiup6jqVursfjqI-EeOFcD9rcp1e8_SFzSLcx7q1wgNB-41qM4zCtHzJEw"
BASE_URL = "https://api.brawlstars.com/v1"


def get_battlelog(player_tag: str):
    tag = player_tag.replace("#", "%23")
    headers = {
        "Authorization": f"Bearer {BRAWL_API_TOKEN}"
    }
    r = requests.get(
        f"{BASE_URL}/players/{tag}/battlelog",
        headers=headers,
        timeout=10
    )
    r.raise_for_status()
    return r.json()["items"]


def find_common_battle(players_tags: list[str], start_time: datetime):
    logs = []
    for tag in players_tags:
        logs.append(get_battlelog(tag))

    for battle in logs[0]:
        battle_time = datetime.strptime(
            battle["battleTime"], "%Y%m%dT%H%M%S.%fZ"
        )

        if battle_time < start_time - timedelta(minutes=10):
            continue

        ids = sorted([p["tag"] for p in battle["battle"]["players"]])

        if all(
            any(
                sorted([p["tag"] for p in b["battle"]["players"]]) == ids
                for b in log
            )
            for log in logs
        ):
            return battle

    return None