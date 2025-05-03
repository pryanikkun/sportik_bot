import asyncio
import logging
import os
from aiogram import Bot
from celery.utils.time import timezone
from django.db.models import OuterRef, Subquery

from web.celery import app
from app_notification.models import Notification, Subscription

bot = Bot(os.getenv('BOT_TOKEN'))
loop = asyncio.new_event_loop()


@app.task
def notification_users_task():
    """Celery задача для уведомления пользователей."""
    now = timezone.now()
    current_day = now.weekday()
    current_hour = now.hour
    current_minute = now.minute
    sub_list = Subscription.objects.filter(
        schedule__hour=current_hour,
        schedule__minute=current_minute,
        schedule__days__contains=current_day,
        is_active=True
    ).annotate(
        next_notification=Subquery(
            Notification.objects
            .filter(type=OuterRef('type'))
            .exclude(id=OuterRef('last_notification_id'))
            .order_by('?').values('id')[:1]
        )
    )

    for sub in sub_list:
        try:
            loop.run_until_complete(
                bot.send_message(
                    chat_id=sub.user.id,
                    text=sub.next_notification.text
                )
            )
            sub.last_notify = now
            sub.last_notification = sub.next_notification
            sub.save()
        except Exception:
            logging.exception(
                f"Ошибка при отправке напоминания для {sub.user.id}"
            )
            continue

