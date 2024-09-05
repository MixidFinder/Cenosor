from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import LinkPreviewOptions, Message

import data_manager.data_manager as dm
from bot.config import logger

router = Router()


class DataDelete(StatesGroup):
    url_choice = State()


@router.message(Command("delete"))
async def product_delete(message: Message, state: FSMContext):
    await state.clear()
    logger.info("Called")
    await state.set_state(DataDelete.url_choice)
    await message.answer("Какой товар хотите удалить?")
    preview_disable = LinkPreviewOptions(is_disabled=True)
    await message.answer(dm.print_products_url(), link_preview_options=preview_disable)


@router.message(DataDelete.url_choice)
async def url_choice(message: Message, state: FSMContext):
    logger.info("Called")
    is_url, url = dm.extract_url(message)
    if is_url:
        if dm.delete_product(url):
            await message.reply(f"Товар {url} удален.")
            await state.clear()
        else:
            await message.answer("Товар не найден в базе данных.")
            await state.clear()
    else:
        await message.reply("Отправьте пожалуйста валидную ссылку.")
