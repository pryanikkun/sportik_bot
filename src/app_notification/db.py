from asgiref.sync import sync_to_async
from .models import Subscription


@sync_to_async
def save_subscription(
        user_id: int,
        schedule: dict,
        type_id: int,
):
    """Сохранение или обновление подписки в БД"""
    Subscription.objects.update_or_create(
        user_id=user_id,
        schedule=schedule,
        type_id=type_id,
        is_active=True,
    )


@sync_to_async
def get_subscription_by_user(
        user_id: int,
):
    """Получение подписки из БД"""
    return Subscription.objects.filter(
        user_id=user_id,
    ).all()


@sync_to_async
def stop_subscription(sub_id: int):
    """Остановка подписки"""
    Subscription.objects.filter(id=sub_id).update(is_active=False)
