import asyncio
import logging
import sys

from bot.dispatcher import dp
from bot.main import bot
from scraper.main import periodic_scraping


async def main() -> None:
    _ = asyncio.create_task(periodic_scraping())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
