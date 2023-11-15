from django.db import models


class Candle(models.Model):
    datetime = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    
    def __str__(self):
        return self.date