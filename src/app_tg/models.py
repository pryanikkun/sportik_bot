from asgiref.sync import sync_to_async
from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name='Дата обновления'
    )


class TGUser(TimeBasedModel):
    id = models.BigIntegerField(
        primary_key=True,
        unique=True,
        db_index=True,
        verbose_name='id Telegram'
    )
    username = models.CharField(
        max_length=64, blank=True, verbose_name='Тег в ТГ'
    )
    first_name = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id}'

    def get_name(self):
        """Получение имя фамилия (мб не нужно)"""
        return f'{self.first_name} {self.last_name}'


@sync_to_async
def save_user(
        id: int,
        username: str,
        first_name: str | None,
        last_name: str | None,
):
    TGUser.objects.update_or_create(
        id=id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
