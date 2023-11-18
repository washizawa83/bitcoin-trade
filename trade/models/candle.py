from django.db import models

from trade.finance.finance import Ticker


class Candle(models.Model):
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
            previous_close_price = cls.objects.last().close
            if previous_close_price is not None:
                open = previous_close_price
                high = mid_price if previous_close_price <= mid_price else previous_close_price
                low = mid_price if mid_price <= previous_close_price else previous_close_price
                close = mid_price
                return open, high, low, close
            else:
                return mid_price, mid_price, mid_price, mid_price
        
        mid_price = ticker.get_mid_price()
        open, high, low, close = get_init_price(mid_price)
            
        cls.objects.create(
            datetime=ticker.get_datetime(),
            open=open,
            high=high,
            low=low,
            close=close
        )
    
    def _update_candle(self, ticker: Ticker, current_candle):
        mid_price = ticker.get_mid_price()
        if current_candle.high < mid_price:
            current_candle.high = mid_price

        elif current_candle.low > mid_price:
            current_candle.low = mid_price

        current_candle.close = mid_price
        current_candle.save()
    
    @classmethod
    def create_candle(cls, ticker: Ticker):
        filtered_candle_from_datetime = cls.objects.filter(datetime=ticker.get_datetime()).last()
        if filtered_candle_from_datetime is not None:
            cls._update_candle(ticker, filtered_candle_from_datetime)
            return False

        cls._new_candle(ticker)
        return True