import time
import logging

from django.core.management.base import BaseCommand

from trade.finance.finance import Ticker
from api.models.candle import Candle
from api.models.indicators import Sma, MaxMin, ParabolicSAR
from api.models.settings import Settings
from trade.finance.trend import Trend, TrendHistory


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.info('start trade')
        is_collected_data = False
        trend: Trend = None
        trend_history = TrendHistory(None, None)
        while not is_collected_data:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            _, is_new_generated = Candle.create_candle(ticker)
            if not is_new_generated or Candle.get_candles_length() < Settings.get_sma_duration() + 1:
                continue
            
            previous_candle = Candle.get_previous_candle()
            Sma.create_sma(previous_candle)
            if Candle.get_candles_length() == Settings.get_sma_duration() + 1:
                trend = Trend.check_initial_trend(previous_candle)
            else:
                trend = Trend.check_trend(previous_candle, trend)
            
            trend_history.change_history(trend)
            if None not in trend_history.get_histories():
                self.max_min = MaxMin.create_max_min(trend_history)
                is_collected_data = True
        
        ParabolicSAR.initial_create_sar(previous_candle, trend)
        logging.info('end collected data')
        return trend, trend_history
    