import time
import logging

from django.core.management.base import BaseCommand

from trade.finance.finance import Ticker
from api.models.candle import Candle
from api.models.indicators import Sma, MaxMin, ParabolicSAR
from api.models.settings import Settings
from trade.finance.trend import Trend, TrendHistory


logger = logging.getLogger('トレードログ')
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    def reset_data(self):
        Candle.objects.all().delete()

    def collection_data(self):
        logger.info('トレード用データ収集中...')
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
                trend = Trend.check_trend(previous_candle, trend.is_up_trend())
            
            trend_history.change_history(trend)
            if None not in trend_history.get_histories():
                self.max_min = MaxMin.create_max_min(trend_history)
                is_collected_data = True
        
        ParabolicSAR.initial_create_sar(previous_candle, trend)
        logger.info('トレード用データ収集終了')
        return trend, trend_history
    
    def trade(self, trend: Trend, trend_history: TrendHistory):
        logger.info('トレード開始')
        # TODO フロントエンドからトレードを終了できるようにする
        while True:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candle, is_new_generated = Candle.create_candle(ticker)

            if not is_new_generated:
                continue
            
            previous_candle = Candle.get_previous_candle()
            Sma.create_sma(previous_candle)
            ParabolicSAR.create_sar(previous_candle)
            trend = Trend.check_trend(previous_candle, trend.is_up_trend())
            trend_history.change_history(trend)
            if trend_history.is_changed():
                MaxMin.create_max_min(trend_history)
    
    def handle(self, *args, **options):
        self.reset_data()
        trend, trend_history = self.collection_data()
        self.trade(trend, trend_history)
