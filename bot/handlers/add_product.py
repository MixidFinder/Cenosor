from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import data_manager.data_manager as dm
from bot.config import logger

router = Router()


class DataAdd(StatesGroup):
    url_choice = State()
    price_choice = State()


@router.message(Command("add"))
async def add_product(message: Message, state: FSMContext):
    logger.info("Called")
    await state.set_state(DataAdd.url_choice)
    await message.answer("Введите URL для добавления товара в базу")


@router.message(DataAdd.url_choice)
async def url_choice(message: Message, state: FSMContext):
    logger.info("Called")
    is_url, url = dm.extract_url(message)
    if is_url:
        if not dm.check_url_in_data(url):
            await state.update_data(url=url)
            await state.set_state(DataAdd.price_choice)
            await message.answer("Введите отслеживаемую цену.")
        else:
            logger.info(f"URL {url} already in data file.")
            await message.reply("Товар уже в базе данных.")
            await state.clear()
    else:
        logger.info("Incorrect URL send.")
        await message.reply("Отправьте пожалуйста валидную ссылку.")


@router.message(DataAdd.price_choice)
async def price_choice(message: Message, state: FSMContext):
    logger.info("Called")
    if message.text.isdigit():
        await state.update_data(track_price=message.text)
        user_data = await state.get_data()
        dm.add_product(**user_data)
        await message.reply(f"Товар '{user_data['url']}' добавлен в базу.")
        await state.clear()
    else:
        logger.info("Sended not int price")
        await message.answer("Введите целое число.")
