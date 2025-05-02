from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app_notification.db import get_subscription_by_user
from app_notification.models import NotificationType, Subscription

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

inline_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=notification_type.name.title(),
                callback_data=notification_type.id
            )
        ] for notification_type in NotificationType.objects.all()
    ]
)

inline_minutes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='00',
                callback_data='0'
            ),
            InlineKeyboardButton(
                text='10',
                callback_data='10'
            ),
            InlineKeyboardButton(
                text='20',
                callback_data='20'
            ),
        ],
        [
            InlineKeyboardButton(
                text='30',
                callback_data='30'
            ),
            InlineKeyboardButton(
                text='40',
                callback_data='40'
            ),
            InlineKeyboardButton(
                text='50',
                callback_data='50'
            )
        ]
    ]
)
inline_hours = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=str(x),
                callback_data=str(x),
            ) for x in range(1, 7)
        ],
        [
            InlineKeyboardButton(
                text=str(x),
                callback_data=str(x),
            ) for x in range(7, 13)
        ],
        [
            InlineKeyboardButton(
                text=str(x),
                callback_data=str(x),
            ) for x in range(13, 19)
        ],
        [
            InlineKeyboardButton(
                text=str(x),
                callback_data=str(x),
            ) for x in range(19, 25)
        ],
    ]
)


def days_keyboard(selected_days: list[int] = None) -> InlineKeyboardMarkup:
    selected_days = selected_days or []
    days = [
        ("Понедельник", 0),
        ("Вторник", 1),
        ("Среда", 2),
        ("Четверг", 3),
        ("Пятница", 4),
        ("Суббота", 5),
        ("Воскресенье", 6)
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Добавляем кнопки с днями
    row = []
    for day_name, day_number in days:
        prefix = "✅ " if day_number in selected_days else ""
        row.append(InlineKeyboardButton(
            text=f"{prefix}{day_name}",
            callback_data=f"day_{day_number}"
        ))
        if len(row) == 2:
            keyboard.inline_keyboard.append(row)
            row = []

    # Добавляем кнопку ежедневно
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="Ежедневно",
            callback_data="days_all"
        )
    ])
    # Добавляем кнопку подтверждения
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="Готово",
            callback_data="days_done"
        )
    ])

    return keyboard


async def inline_unsub(user_id: int):
    """Ленивая клавиатура для отписки"""
    subscriptions = await get_subscription_by_user(user_id)
    return InlineKeyboardMarkup(
        inline_keyboards=[
            [
                InlineKeyboardButton(
                    text=f"{sub.type.name.title()}",
                    callback_data=f"unsub_{sub.id}"
                )
            ] for sub in subscriptions
        ]
    )

# def inline_unsub(sub_list: list | None = None) -> InlineKeyboardMarkup:
#     """Создание инлайн-клавиатуры для отписки от подписки."""
#     subscriptions = await get_subscription_by_user(user_id)
#     sub_list = sub_list or []
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[])
#
#     # Добавляем кнопки с подписками
#     for sub in subscriptions:
#         prefix = "✅ " if sub.id in sub_list else ""
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=f"{prefix}{sub.type.name.title()}",
#                 callback_data=f"unsubscribe_{sub.id}"
#             )
#         )
#
#     # Добавляем кнопку отмены
#     keyboard.add(
#         InlineKeyboardButton(
#             text="Готово",
#             callback_data="done"
#         )
#     )
#     keyboard.add(
#         InlineKeyboardButton(
#             text="Отмена",
#             callback_data="cancel"
#         )
#     )
#
#     return keyboard
