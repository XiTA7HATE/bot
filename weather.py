"""
handlers/weather.py — real weather via OpenWeatherMap API
"""

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import WEATHER_API_KEY

router = Router()

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

CONDITION_ICONS = {
    "clear":        "☀️",
    "clouds":       "☁️",
    "rain":         "🌧",
    "drizzle":      "🌦",
    "thunderstorm": "⛈",
    "snow":         "❄️",
    "mist":         "🌫",
    "fog":          "🌫",
    "haze":         "🌫",
}


def get_icon(condition: str) -> str:
    return CONDITION_ICONS.get(condition.lower(), "🌡")


def wind_direction(deg: int) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(deg / 45) % 8]


async def fetch_weather(city: str) -> dict | None:
    params = {
        "q":     city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


@router.message(Command("weather"))
@router.message(lambda m: m.text == "🌤 Weather")
async def cmd_weather(message: Message) -> None:
    if message.text == "🌤 Weather":
        await message.answer("Send a city name:\n<code>/weather Kyiv</code>")
        return

    city = message.text.removeprefix("/weather").strip()
    if not city:
        await message.answer("Usage: <code>/weather Kyiv</code>")
        return

    await message.answer("⏳ Fetching weather...")

    data = await fetch_weather(city)
    if not data:
        await message.answer(f"❌ City <b>{city}</b> not found.")
        return

    condition = data["weather"][0]["main"]
    desc      = data["weather"][0]["description"].capitalize()
    temp      = data["main"]["temp"]
    feels     = data["main"]["feels_like"]
    humidity  = data["main"]["humidity"]
    wind_spd  = data["wind"]["speed"]
    wind_deg  = data["wind"].get("deg", 0)
    icon      = get_icon(condition)

    await message.answer(
        f"{icon} <b>{data['name']}, {data['sys']['country']}</b>\n\n"
        f"🌡 <b>{temp:+.1f}°C</b>  (feels like {feels:+.1f}°C)\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind: {wind_spd} m/s {wind_direction(wind_deg)}\n"
        f"📋 {desc}"
    )
