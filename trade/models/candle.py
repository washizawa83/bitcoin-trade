from django.db import models

from trade.finance.finance import Ticker


class Candle(models.Model):
    is_new_candle = False
    datetime = models.DateTimeField(unique=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    
    def __str__(self):
         return f"{self.datetime}"
    
    @classmethod
    def _new_candle(cls, ticker: Ticker):
        def get_init_price(mid_price):
            previous_candle = cls.objects.last()
            if previous_candle is not None:
                previous_close_price = cls.objects.last().close
                open = previous_close_price
                high = mid_price if previous_close_price <= mid_price else previous_close_price
                low = mid_price if mid_price <= previous_close_price else previous_close_price
                close = mid_price
                return open, high, low, close
            else:
                return mid_price, mid_price, mid_price, mid_price
        
        mid_price = ticker.get_mid_price()
        open, high, low, close = get_init_price(mid_price)
            
        return cls.objects.create(
            datetime=ticker.get_datetime(),
            open=open,
            high=high,
            low=low,
            close=close
        )
    
    @classmethod
    def _update_candle(cls, ticker: Ticker, current_candle):
        mid_price = ticker.get_mid_price()
        if current_candle.high < mid_price:
            current_candle.high = mid_price

        elif current_candle.low > mid_price:
            current_candle.low = mid_price

        current_candle.close = mid_price
        current_candle.save()
        return current_candle
    
    @classmethod
    def create_candle(cls, ticker: Ticker):
        filtered_candle_from_datetime = cls.objects.filter(datetime=ticker.get_datetime()).last()
        if filtered_candle_from_datetime is not None:
            updated_candle = cls._update_candle(ticker, filtered_candle_from_datetime)
            return updated_candle, False

        new_candle = cls._new_candle(ticker)
        return new_candle, True

    @classmethod
    def get_candles_length(cls) -> int:
        return cls.objects.all().count()