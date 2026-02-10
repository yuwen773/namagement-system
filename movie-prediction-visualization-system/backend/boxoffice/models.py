from django.db import models
from django.utils import timezone


class BoxOfficeRecord(models.Model):
    """票房记录模型"""

    movie = models.ForeignKey(
        'movies.Movie',
        on_delete=models.CASCADE,
        related_name='boxoffice_records',
        verbose_name='影片'
    )
    cinema = models.ForeignKey(
        'cinemas.Cinema',
        on_delete=models.CASCADE,
        related_name='boxoffice_records',
        verbose_name='影院'
    )
    record_date = models.DateField('记录日期')
    daily_box_office = models.DecimalField(
        '当日票房（元）',
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    screening_count = models.IntegerField('排片场次', default=0)
    audience_count = models.IntegerField('观影人次', default=0)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'boxoffice_records'
        verbose_name = '票房记录'
        verbose_name_plural = '票房管理'
        unique_together = ('movie', 'cinema', 'record_date')
        ordering = ['-record_date', '-created_at']

    def __str__(self):
        return f"{self.movie.title} - {self.cinema.name} - {self.record_date}"
