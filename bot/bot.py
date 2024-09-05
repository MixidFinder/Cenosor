import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

from bot.command_list import main_cmds
from bot.config import logger
from bot.handlers import update_product

from .handlers import add_product, delete_product, hello_start, view_data

ALLOWED_UPDATES = ["message, edited_message"]


async def main():
    load_dotenv(find_dotenv())

    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        hello_start.router,
        add_product.router,
        delete_product.router,
        update_product.router,
        view_data.router,
    )

    logger.info("Bot launched.")
    await bot.set_my_commands(commands=main_cmds)

    try:
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
