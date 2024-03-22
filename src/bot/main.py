from aiogram import Bot
from aiogram.enums import ParseMode

from core.config import settings

bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
