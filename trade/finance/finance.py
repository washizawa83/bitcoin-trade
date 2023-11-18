import datetime

from trade.finance.api import ApiClient
from trade.finance.utils.date_util import ConvertDate
from trade.models.settings import Settings


class Ticker:
    def __init__(self, ticker_datetime: str, mid_price: float, volume: int) -> None:
        self._datetime = ticker_datetime
        self._mid_price = mid_price
        self._volume = volume

    def get_datetime(self) -> str:
        return self._datetime

    def get_mid_price(self) -> float:
        return self._mid_price

    def get_volume(self) -> float:
        return self._volume

    @classmethod
    def _get_ticker_mid_price(cls, ticker) -> float:
        return (ticker['best_ask'] + ticker['best_bid']) / 2

    @classmethod
    def _get_ticker_volume(cls, ticker) -> float:
        return ticker['volume']

    @classmethod
    def create_ticker(cls):
        api_client = ApiClient()
        ticker = api_client.fetch_ticker()
        settings = Settings.objects.first()
        if ticker:
            ticker_timestamp = datetime.datetime.timestamp(
                ticker['timestamp']) + datetime.timedelta(hours=9)
            ticker_datetime = ConvertDate.convert_datetime_duration(
                ticker_timestamp, settings.get_duration_name(settings.duration))
            mid_price = cls._get_ticker_mid_price(ticker)
            volume = cls._get_ticker_volume(ticker)

            return cls(ticker_datetime, mid_price, volume)
