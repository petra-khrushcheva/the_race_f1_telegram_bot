from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.models import ChatID  # noqa
from bot.router import router
from core import settings
from scraper.services import delete_all_articles, initial_scraping

bot = Bot(
    token=settings.bot_token.get_secret_value(), parse_mode=ParseMode.HTML
)

dp = Dispatcher()
dp.startup.register(initial_scraping)
dp.shutdown.register(delete_all_articles)
dp.include_router(router)
