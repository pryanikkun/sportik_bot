import logging
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
import tg_bot.keyboards.reply as rep_kb

from app_tg.db import save_user

router_start = Router()


@router_start.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""
    try:
        await save_user(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    except Exception:
        logging.exception(
            'Ошибка сохранения пользователя. Данные: '
            f'{message.from_user.id}, '
            f'{message.from_user.username}, '
            f'{message.from_user.first_name}, '
            f'{message.from_user.last_name}'
        )

        await message.reply(
            'Привет!\n '
            'Прости, у меня какие-то проблемы с твоими данными, попробуй позже'
        )
    await message.reply(
        "Приветики-пистолетики!\n "
        "I'm your bot from Foxland.\n"
        "Тыкни на /help, чтобы узнать, что я умею",
        reply_markup=rep_kb.main,
    )
