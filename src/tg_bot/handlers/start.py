from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
import tg_bot.keyboards.reply as rep_kb

router_start = Router()


@router_start.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        "Приветики-пистолетики! I'm your bot from Foxland."
        "\n\n"
        "тыкни на /help, чтобы узнать, что я умею",
        reply_markup=rep_kb.main,
    )
    print(
        f"User {message.from_user.id} started the bot.\n"
        f"User info: {message.from_user}"
    )
