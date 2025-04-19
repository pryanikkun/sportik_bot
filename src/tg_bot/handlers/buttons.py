from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import tg_bot.keyboards.inline as in_kb

router_buttons = Router()


@router_buttons.message(Command('need_buttons'))
async def cmd_buttons(message: Message):
    await message.reply(
        "Держи (づ◡﹏◡)づ",
        reply_markup=in_kb.inline_callback,
    )
    print(
        f"User {message.from_user.id} started the bot.\n"
        f"User info: {message.from_user}"
    )


@router_buttons.message(Command('inline'))
async def cmd_buttons_oth(message: Message):
    await message.reply(
        "Держи другие кнопачки (づ◡﹏◡)づ",
        reply_markup=in_kb.inline_urls,
    )
    print(
        f"User {message.from_user.id} started the bot.\n"
        f"User info: {message.from_user}"
    )


@router_buttons.callback_query(F.data == 'buttons')
async def buttons(callback: CallbackQuery):
    await callback.answer("Вы тыкнули на кнопку (￣▽￣)ノ")
    await callback.message.edit_text(
        "(づ◡﹏◡)づ",
        reply_markup=in_kb.inline_urls,
    )
    print(
        f"User {callback.message.from_user.id} started the bot.\n"
        f"User info: {callback.message.from_user}"
    )
