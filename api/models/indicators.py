from django.db import models
from django.db.models import Avg, Min

from api.models.candle import Candle
from api.models.settings import Settings
from trade.finance.trend import Trend, TrendHistory


class Sma(models.Model):
    price = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)

    def __str__(self):
        return self.candle.datetime

    @classmethod
    def get_average_price(cls):
        duration = Settings.get_sma_duration()
        # 1つ前のCandleからduration分Candle取得
        candles = Candle.objects.order_by('-datetime')[1:duration + 1]
        average_price = candles.aggregate(Avg('close'))
        return average_price['close__avg']

    @classmethod
    def create_sma(cls, previous_candle: Candle):
        average_price = cls.get_average_price()
        return cls.objects.create(
            candle=previous_candle,
            price=average_price
        )


class MaxMin(models.Model):
    price = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.candle.datetime)

    @classmethod
    def _extraction_max_min_from_trend_histories(cls, trend_history: TrendHistory) -> Candle:
        histories = trend_history.get_histories()
        candles_between_trend = Candle.objects.filter(datetime__range=(histories[1].get_date(), histories[0].get_date()))

        if histories[0].is_up_trend():
            # 範囲内のlowフィールドから値が一番小さいQuerySet取得
            min_price_candle = candles_between_trend.order_by('low').first()
            return min_price_candle, min_price_candle.low
        else:
            # 範囲内のhighフィールドから値が一番大きいQuerySet取得
            max_price_candle = candles_between_trend.order_by('-high').first()
            return max_price_candle, max_price_candle.high

    @classmethod
    def create_max_min(cls, trend_history: TrendHistory):
        max_min_candle, max_min_price = cls._extraction_max_min_from_trend_histories(trend_history)
        return cls.objects.create(
            candle=max_min_candle,
            price=max_min_price
        )


class ParabolicSAR(models.Model):
    step = 0.02
    maximum = 0.2

    price = models.FloatField()
    is_up_trend = models.BooleanField()
    updated_price = models.FloatField()
    current_step = models.FloatField()
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE)

    def __str__(self):
        return self.candle.datetime

    # SAR = 前足のSAR + AF * (EP - 前足のSAR)
    @classmethod
    def _calc_sar(cls, previous_sar):
        return previous_sar.price + cls.step * (previous_sar.updated_price - previous_sar.price)

    @classmethod
    def _convert_sar(cls, previous_candle, current_sar):
        updated_price = 0
        if current_sar.is_up_trend:
            updated_price = previous_candle.low
        else:
            updated_price = previous_candle.high

        cls.objects.create(
            candle=previous_candle,
            price=current_sar.updated_price,
            is_up_trend=not current_sar.is_up_trend,
            updated_price=updated_price,
            current_step=cls.step
        )

    @classmethod
    def initial_create_sar(cls, previous_candle: Candle, trend: Trend):
        prevent_sar = MaxMin.objects.last().price
        updated_price = 0

        if trend.is_up_trend():
            updated_price = previous_candle.high
        else:
            updated_price = previous_candle.low
        
        return cls.objects.create(
            candle=previous_candle,
            price=prevent_sar,
            is_up_trend=trend.is_up_trend(),
            updated_price=updated_price,
            current_step=cls.step
        )
    
    @classmethod
    def create_sar(cls, previous_candle: Candle):
        current_sar = cls.objects.last()
        updated_price = 0
        step = cls.step

        if current_sar.is_up_trend:
            # 転換した場合
            if previous_candle.low < current_sar.price:
                return cls._convert_sar(previous_candle, current_sar)

            if current_sar.updated_price < previous_candle.high:
                updated_price = previous_candle.high
                step = current_sar.step if cls.maximum <= current_sar.step else current_sar.step + cls.step
        # 下降トレンド
        else:
            # 転換した場合
            if current_sar.price < previous_candle.high:
                return cls._convert_sar(previous_candle, current_sar)

            if previous_candle.low < current_sar.updated_price:
                updated_price = previous_candle.low
                step = current_sar.step if cls.maximum <= current_sar.step else current_sar.step + cls.step

        return cls.objects.create(
            candle=previous_candle,
            price=cls._calc_sar(current_sar),
            is_up_trend=current_sar.is_up_trend,
            updated_price=updated_price,
            current_step=step
        )
