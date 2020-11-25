from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """スケジュール"""
    description = models.TextField('コメント', blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.description
