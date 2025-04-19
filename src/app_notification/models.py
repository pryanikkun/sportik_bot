from django.db import models
from app_tg.models import TGUser


class NotificationType(models.Model):
    # class Type(models.TextChoices):
    #     WATER = 'WATER'
    #     SPORT = 'SPORT'
    #     CHALLENGE = 'CHALLENGE'
    #     MOTIVATION = 'MOTIVATION'
    #     ALL = 'ALL'
    #     EVENT = 'EVENT'

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Тип напоминания'
        verbose_name_plural = 'Типы напоминания'



class Notification(models.Model):


    class Meta:
        verbose_name = 'Напоминалка'
        verbose_name_plural = 'Напоминалки'