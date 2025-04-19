from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


router_help = Router()


@router_help.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "Смотри, что могу <(￣︶￣)>"
        "\n\n"
        "/start - Запустить меня\n"
        "/help - Получить от меня помощь\n"
        "/get_photo - Получить прекрасное фото\n"
        "/need_buttons - Получить кнопки в клаве\n"
        "/inline - Получить кнопки под сообщением\n"
        "/registrate - Регистрация\n"
        "А ещё можешь выслать свою фотачку, и получишь мою объективную оценку\n"
    )
