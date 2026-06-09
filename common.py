"""
handlers/common.py — /start, /help, main menu
"""

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧮 Calculator"), KeyboardButton(text="🌤 Weather")],
        [KeyboardButton(text="📝 My Notes"),   KeyboardButton(text="ℹ️ Help")],
    ],
    resize_keyboard=True,
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name
    await message.answer(
        f"Hey, <b>{name}</b>! 👋\n\n"
        "I'm a multi-tool bot. Here's what I can do:\n\n"
        "🧮 <b>Calculator</b> — evaluate any math expression\n"
        "🌤 <b>Weather</b> — current weather for any city\n"
        "📝 <b>Notes</b> — save and recall personal notes\n\n"
        "Use the keyboard below or type /help for commands.",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(Command("help"))
@router.message(lambda m: m.text == "ℹ️ Help")
async def cmd_help(message: Message) -> None:
    await message.answer(
        "<b>Available commands:</b>\n\n"
        "/start — main menu\n"
        "/calc <code>2 + 2 * 10</code> — calculate expression\n"
        "/weather <code>Kyiv</code> — get weather\n"
        "/note <code>text</code> — save a note\n"
        "/notes — list all your notes\n"
        "/clear — delete all notes\n"
    )
