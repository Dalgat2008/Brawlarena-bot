from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Создать матч", callback_data="match_create")],
        [InlineKeyboardButton(text="📥 Войти в матч", callback_data="match_join")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    ])


def choose_mode():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Solo", callback_data="mode_solo"),
            InlineKeyboardButton(text="Duel", callback_data="mode_duel"),
        ]
    ])


def join_match(match_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Присоединиться",
                callback_data=f"join_{match_id}",
            )
        ]
    ])