from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramForbiddenError

from bot.services import save_chat_id_to_db, send_initial_articles
from scraper.services import initial_scraping, delete_all_articles

dp = Dispatcher()
dp.startup.register(initial_scraping)
dp.shutdown.register(delete_all_articles)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with "/start" command
    """
    chat_id = message.chat.id
    await save_chat_id_to_db(chat_id=chat_id)
    await send_initial_articles(message=message)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with "/help" command
    """
    try:
        await message.answer(
            "Этот бот присылает вам новые статьи о Формуле 1 с сайта "
            "The Race по мере их выхода"
        )
    except TelegramForbiddenError:
        pass


@dp.message()
async def any_message_handler(message: Message) -> None:
    """
    This handler receives any other messages
    """
    link_button = InlineKeyboardButton(
        text="The Race", url="https://www.the-race.com/formula-1/"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[link_button]])
    try:
        await message.reply(
            text="Новых статей пока нет. Можете проверить сами:",
            reply_markup=keyboard,
        )
    except TelegramForbiddenError:
        pass
