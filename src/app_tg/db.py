from asgiref.sync import sync_to_async
from .models import TGUser


@sync_to_async
def save_user(
        id: int,
        username: str,
        first_name: str | None,
        last_name: str | None,
):
    """Сохранение или обновления пользователя в БД."""
    TGUser.objects.update_or_create(
        id=id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
    )
