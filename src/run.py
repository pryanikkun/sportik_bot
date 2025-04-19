import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from django.conf import settings
from tg_bot.dispatcher import dp


async def main_bot():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print("Starting bot...")
        asyncio.run(main_bot())
    except KeyboardInterrupt:
        print("Bot stopped")
