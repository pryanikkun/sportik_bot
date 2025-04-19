from django.db import models
from app_tg.models import TimeBasedModel, TGUser


class Competition(models.Model):
    name = models.CharField(
        max_length=512, verbose_name='Название соревнования'
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание соревнования'
    )
    start_date = models.DateTimeField(
        null=True,
        verbose_name='Дата начала соревнования'
    )
    end_date = models.DateTimeField(
        null=True,
        verbose_name='Дата окончания соревнования'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активно'
    )

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        return f'{self.name} ({self.start_date} - {self.end_date})'


class Score(TimeBasedModel):
    score = models.IntegerField(default=0, verbose_name='Счёт')
    user = models.OneToOneField(
        TGUser, on_delete=models.CASCADE, related_name='scores',
        verbose_name='Пользователь'
    )
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='scores',
        verbose_name='Соревнование'
    )

    class Meta:
        verbose_name = 'Cчёт'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return (
            f'{self.user.username}({self.competition}): {self.score}'
        )
