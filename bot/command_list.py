from aiogram.types import BotCommand

main_cmds = [
    BotCommand(command="view", description="Посмотреть все товары и цены"),
    BotCommand(command="add", description="Добавить товар"),
    BotCommand(command="delete", description="Удалить товар"),
    BotCommand(command="update", description="Обновить отслеживаемую цену"),
]
