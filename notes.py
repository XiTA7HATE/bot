"""
handlers/notes.py — per-user notes stored in memory
"""

from collections import defaultdict
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# { user_id: ["note1", "note2", ...] }
_notes: dict[int, list[str]] = defaultdict(list)

MAX_NOTES = 10


@router.message(Command("note"))
@router.message(lambda m: m.text == "📝 My Notes")
async def cmd_note(message: Message) -> None:
    if message.text == "📝 My Notes":
        await cmd_list_notes(message)
        return

    text = message.text.removeprefix("/note").strip()
    if not text:
        await message.answer(
            "Usage: <code>/note Buy milk</code>\n"
            "View all: /notes\n"
            "Delete all: /clear"
        )
        return

    uid = message.from_user.id
    if len(_notes[uid]) >= MAX_NOTES:
        await message.answer(f"❌ Max {MAX_NOTES} notes reached. Use /clear to delete all.")
        return

    _notes[uid].append(text)
    idx = len(_notes[uid])
    await message.answer(f"✅ Note #{idx} saved.")


@router.message(Command("notes"))
async def cmd_list_notes(message: Message) -> None:
    uid   = message.from_user.id
    items = _notes[uid]

    if not items:
        await message.answer("📭 No notes yet.\nAdd one: <code>/note Your text here</code>")
        return

    lines = "\n".join(f"  {i}. {note}" for i, note in enumerate(items, 1))
    await message.answer(
        f"📝 <b>Your notes</b> ({len(items)}/{MAX_NOTES}):\n\n{lines}"
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message) -> None:
    uid = message.from_user.id
    count = len(_notes[uid])
    _notes[uid].clear()
    await message.answer(f"🗑 Deleted {count} note(s).")
