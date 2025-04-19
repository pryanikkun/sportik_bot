from django.contrib.auth.models import User
from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')


class TGUser(TimeBasedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='пользователь')
    tg_id = models.BigIntegerField(unique=True, db_index=True, verbose_name='id Telegram')
    username = models.CharField(
        max_length=64, verbose_name='Тег в ТГ'
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
        return f'{self.tg_id}'

    def get_name(self):
        """Получение имя фамилия (мб не нужно)"""
        return f'{self.first_name} {self.last_name}'
