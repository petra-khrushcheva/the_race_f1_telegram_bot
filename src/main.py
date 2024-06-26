import asyncio
import logging
import sys

from bot import bot, dp
from scraper.services import periodic_scraping


async def main() -> None:
    asyncio.create_task(periodic_scraping(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
