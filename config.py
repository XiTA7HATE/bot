"""
config.py — all settings in one place
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
