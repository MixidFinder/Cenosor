from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import LinkPreviewOptions, Message

import data_manager.data_manager as dm
from bot.config import logger

router = Router()


class DataUpdate(StatesGroup):
    url_choice = State()
    track_price_choice = State()


@router.message(Command("update"))
async def update_track_price(message: Message, state: FSMContext):
    logger.info("Called")
    await state.set_state(DataUpdate.url_choice)
    await message.answer("К какому товару хотите изменить отслеживаемую цену?")
    preview_disable = LinkPreviewOptions(is_disabled=True)
    await message.answer(dm.print_products_url(), link_preview_options=preview_disable)


@router.message(DataUpdate.url_choice)
async def url_choice(message: Message, state: FSMContext):
    logger.info("Called")
    is_url, url = dm.extract_url(message)
    if is_url:
        await state.set_state(DataUpdate.track_price_choice)
        await state.update_data(url=url)
        await message.reply("Введите новую отслеживаемую цену.")
    else:
        await message.reply("Отправьте пожалуйста валидную ссылку.")


@router.message(DataUpdate.track_price_choice)
async def track_price_choice(message: Message, state: FSMContext):
    logger.info("Called")
    data = await state.get_data()
    url = data.get("url", "")
    if message.text.isdigit():
        dm.update_track_price(url, message.text)
        await message.reply("Отслеживаемая цена обновлена.")
        await state.clear()
    else:
        logger.info("Sended not int price")
        await message.reply("Введите целое число.")
