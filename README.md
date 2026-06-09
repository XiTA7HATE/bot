# Telegram Multi-Tool Bot

A Telegram bot built with **aiogram 3** and **aiohttp**.

## Features
- 🧮 **Calculator** — safe AST-based math evaluator (no `eval`)
- 🌤 **Weather** — real-time data from OpenWeatherMap
- 📝 **Notes** — per-user note storage with commands

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_openweathermap_key
```

Run:
```bash
python bot.py
```

## Project structure
```
tgbot/
├── bot.py              # entry point
├── config.py           # settings from .env
├── requirements.txt
└── handlers/
    ├── common.py       # /start, /help, keyboard
    ├── calculator.py   # /calc
    ├── weather.py      # /weather
    └── notes.py        # /note, /notes, /clear
```

## Commands
| Command | Description |
|---|---|
| `/start` | Main menu |
| `/calc 2+2*10` | Evaluate math expression |
| `/weather Kyiv` | Current weather |
| `/note Buy milk` | Save a note |
| `/notes` | List all notes |
| `/clear` | Delete all notes |
