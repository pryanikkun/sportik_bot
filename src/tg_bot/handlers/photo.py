from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router_photo = Router()


@router_photo.message(F.photo)
async def photo_handler(message: Message):
    await message.answer(
        f"Это что тут такое красивое! Сюююдааа\n "
    )
    print(f"ID: {message.photo[-1].file_id}")


@router_photo.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(
         photo='AgACAgIAAxkBAAICPGfyoxnfcC4V3DJCOPzz54DqBG_iAAIV-'
               'zEbGHeYS5h-16imNmH8AQADAgADbQADNgQ',
         caption='Какой лев этот тигр!'
    )
