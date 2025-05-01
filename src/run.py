import django
import asyncio
import os
from aiogram import Bot


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "web.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


async def main_bot():
    setup_django()
    from django.conf import settings
    bot = Bot(token=settings.BOT_TOKEN)
    from tg_bot.dispatcher import dp
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print("Starting bot...")
        asyncio.run(main_bot())
    except KeyboardInterrupt:
        print("Bot stopped")
