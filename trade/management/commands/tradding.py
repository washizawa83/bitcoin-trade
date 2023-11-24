import time
from django.core.management.base import BaseCommand

from trade.finance.finance import Ticker
from trade.models import Settings
from trade.models.candle import Candle


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('トレード開始')
        is_collected_data = False
        while not is_collected_data:
            time.sleep(1)
            ticker = Ticker.create_ticker()
            candle, is_new_generated = Candle.create_candle(ticker)
            if not is_new_generated or Candle.get_candles_length() < Settings.get_sma_duration() + 1:
                continue
            
            print('new candle!!')
            is_collected_data = True