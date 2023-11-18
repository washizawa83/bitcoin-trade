from django.db import models

from trade.models.candle import Candle


class Sma(models.Model):
    price = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)


class MaxMin(models.Model):
    price = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)


class ParabolicSAR(models.Model):
    price = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)