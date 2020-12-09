from django.db import models
from django.utils import timezone


ALIGN = (
    ('left', 'left'),
    ('center', 'center'),
    ('right', 'right')
)


class Schedule(models.Model):
    """スケジュール"""
    align = models.CharField('文字揃え', max_length=8, choices=ALIGN, default='left')
    description = models.TextField('コメント', blank=True)
    memo = models.TextField('メモ', blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.description
