from aiogram import Bot
from aiogram.enums import ParseMode

from bot.models import ChatID  # noqa
from core.config import settings

bot = Bot(
    token=settings.bot_token.get_secret_value(), parse_mode=ParseMode.HTML
)
