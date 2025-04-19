from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/start')],
        [
            KeyboardButton(text='/help'),
            KeyboardButton(text='/get_photo')
        ],
        [
            KeyboardButton(text='/need_buttons'),
            KeyboardButton(text='/inline')
        ],
        [KeyboardButton(text='/reg')]
    ],
    resize_keyboard=True,
    input_field_placeholder="(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
)