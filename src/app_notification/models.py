from django.db import models
from django.utils.timezone import now
from app_tg.models import TGUser, TimeBasedModel


class NotificationType(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name = 'Тип напоминалки'
        verbose_name_plural = 'Типы напоминалок'

    def __str__(self):
        return self.name
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


class Subscription(TimeBasedModel):
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
    last_notify = models.DateTimeField(
        null=True,
        blank=True,
        default=now,
        verbose_name='Дата последнего уведомления',
    )
    last_notification = models.ForeignKey(
        Notification,
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name='Последнее уведомление',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'type'],
                name='unique_user_type',
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.type.name}'

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


