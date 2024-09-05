from aiogram import Router
from aiogram.filters import Command
from aiogram.types import LinkPreviewOptions, Message

import data_manager.data_manager as dm
from bot.config import logger

router = Router()


@router.message(Command("view"))
async def view_product(message: Message):
    logger.info("Called")
    data = dm.load_data()
    preview_disable = LinkPreviewOptions(is_disabled=True)
    await message.answer(dm.print_all(data), link_preview_options=preview_disable)
