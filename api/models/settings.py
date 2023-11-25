from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Settings(models.Model):
    DURATIONS = (
        (1, '10S'),
        (2, '1M'),
        (3, '5M'),
        (4, '10M'),
        (5, '15M'),
        (6, '1H'),
        (7, '4H')
    )
    duration = models.PositiveIntegerField(choices=DURATIONS)
    sma_duration = models.PositiveIntegerField(default=5, validators=[MinValueValidator(2), MaxValueValidator(240)])
    parabolic_sar_step = models.FloatField(default=0.02)
    parabolic_sar_maximum = models.FloatField(default=0.2)

    def __str__(self):
        return 'トレード設定'
    
    def get_duration_name(self, duration: int) -> str:
        duration_dict = dict(self.DURATIONS)
        return duration_dict[duration]
    
    @classmethod
    def get_sma_duration(cls):
        return cls.objects.get(id=1).sma_duration
    
    