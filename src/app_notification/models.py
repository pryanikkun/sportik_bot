from django.db import models
from app_tg.models import TGUser


class NotificationType(models.Model):
    type = models.CharField(max_length=64, null=False, blank=False)
    # WATER = 'WATER'
    # SPORT = 'SPORT'
    # CHALLENGE = 'CHALLENGE'
    # MOTIVATION = 'MOTIVATION'
    # ALL = 'ALL'
    # EVENT = 'EVENT'


class Notification(models.Model):
    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = 'Напоминалка'
        verbose_name_plural = 'Напоминалки'


class Subscription(models.Model):
    """Подписка пользователя на тип уведомлений"""
    user = models.ForeignKey(
        TGUser, on_delete=models.CASCADE, related_name='subscriptions'
    )
    schedule = models.JSONField(default=dict, verbose_name='Расписание')
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - {self.type}'

    @staticmethod
    def get_crontab_schedule(
        minute: int,
        hour: int,
        week_days: list
    ) -> dict:
        """Возвращает расписание в формате crontab"""
        return {
            'minute': minute,
            'hour': hour,
            'days_of_week': week_days,
        }


