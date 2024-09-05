from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import data_manager.data_manager as dm
from bot.config import logger

router = Router()


@router.message(Command("start"))
async def start_bot(message: Message):
    logger.info(f"Start command received from user {message.from_user.id}")
    dm.init_data()
    await message.reply("Привет, посмотрите команды в меню для работы с ботом.")
