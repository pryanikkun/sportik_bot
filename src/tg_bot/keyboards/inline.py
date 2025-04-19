from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

inline_callback = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Кнопки',
                callback_data='buttons'
            ),
            InlineKeyboardButton(
                text='Справка',
                callback_data='help'
            )
        ]
    ]
)

inline_urls = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Youtube',
                url='https://www.youtube.com/watch?v=onIZKvf7qU8'
            ),
            InlineKeyboardButton(
                text='Справка',
                url='https://avatars.mds.yandex.net/i?id=64c61dccbf99c6ffb11d899e34438008_l-11942308-images-thumbs&n=13'
            )
        ]
    ]
)
