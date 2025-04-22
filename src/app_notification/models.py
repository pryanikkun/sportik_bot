from django.db import models
from app_tg.models import TGUser


class NotificationType(models.TextChoices):
    WATER = 'WATER'
    SPORT = 'SPORT'
    CHALLENGE = 'CHALLENGE'
    MOTIVATION = 'MOTIVATION'
    ALL = 'ALL'
    EVENT = 'EVENT'


class Notification(models.Model):
    type = models.CharField(max_length=64, choices=NotificationType.choices)
    text = models.TextField()

    class Meta:
        verbose_name = 'Напоминалка'
        verbose_name_plural = 'Напоминалки'


class NotificationSchedule(models.Model):
    DAILY = 'daily'
    CUSTOM = 'custom'
    NOPE = 'no'

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (CUSTOM, 'Произвольное расписание'),
        (NOPE, 'Не оповещать')
    ]

    is_active = models.BooleanField(default=True, verbose_name='Активно')

    # Основные параметры расписания
    periodicity = models.CharField(
        max_length=10,
        choices=PERIODICITY_CHOICES,
        default=NOPE,
        verbose_name='Периодичность'
    )

    # Для ежедневных/еженедельных оповещений
    minute = models.CharField(
        max_length=50, default='*', verbose_name='Минуты'
    )
    hour = models.CharField(
        max_length=50, default='*', verbose_name='Часы'
    )
    week_days = models.CharField(
        max_length=50, default='*', verbose_name='Дни недели'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.get_periodicity_display()} "
            f"{self.get_schedule()}"
        )

    def get_crontab_schedule(self):
        """Возвращает расписание в формате crontab"""
        if self.periodicity == self.CUSTOM:
            return {
                'minute': self.minute,
                'hour': self.hour,
                'day_of_month': "*",
                'month_of_year': "*",
                'day_of_week': self.week_days,
            }
        elif self.periodicity == self.DAILY:
            return {
                'minute': self.minute,
                'hour': self.hour,
                'day_of_week': '*',
            }

    def get_schedule(self):
        return (
            f"{self.minute} {self.hour} * * {self.week_days}"
        )

    def get_periodicity_display(self):
        """Возвращает строку с периодичностью"""
        if self.periodicity == self.DAILY:
            return 'Ежедневно'
        elif self.periodicity == self.CUSTOM:
            return 'Произвольное расписание'
        return 'Не оповещать'

    class Meta:
        verbose_name = 'Расписание оповещений'
        verbose_name_plural = 'Расписания оповещений'


class Subscription(models.Model):

    user = models.ForeignKey(
        TGUser, on_delete=models.CASCADE, related_name='subscriptions'
    )
    schedule = models.ForeignKey(
        NotificationSchedule,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    type = models.CharField(
        max_length=64,
        choices=NotificationType.choices,
        verbose_name='Тип уведомления'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - {self.type}'
