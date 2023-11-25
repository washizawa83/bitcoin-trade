from typing import Optional

from api.models.candle import Candle


class Trend:
    def __init__(self, change_trend_datetime: str, is_up_trend: bool) -> None:
        self._datetime = change_trend_datetime
        self._trend = is_up_trend

    def is_up_trend(self):
        return self._trend

    def get_date(self):
        return self._datetime

    @classmethod
    def check_initial_trend(cls, previous_candle: Candle):
        if not hasattr(previous_candle, 'sma'):
            return None
        
        sma_price = previous_candle.sma.price
        default_price = (previous_candle.high + previous_candle.low) / 2

        return cls(previous_candle.datetime, True if sma_price < default_price else False)

    @classmethod
    def check_trend(cls, previous_candle: Candle, current_trend: bool):
        sma_price = previous_candle.sma.price
        if current_trend:
            if previous_candle.high < sma_price:
                return cls(previous_candle.datetime, not current_trend)
        else:
            if previous_candle.low > sma_price:
                return cls(previous_candle.datetime, not current_trend)
        return cls(previous_candle.datetime, current_trend)


class TrendHistory:
    def __init__(self, prevent_trend: Optional[Trend] = None, current_trend: Optional[Trend] = None) -> None:
        self._current_trend = current_trend
        self._prevent_trend = prevent_trend
        self._is_changed = False

    def is_changed(self) -> bool:
        return self._is_changed

    def change_history(self, current_trend: Optional[Trend]):
        if self._current_trend is None:
            self._current_trend = current_trend
        if self._current_trend.is_up_trend() == current_trend.is_up_trend():
            self._is_changed = False
            return

        self._prevent_trend = self._current_trend
        self._current_trend = current_trend
        self._is_changed = True

    def get_histories(self) -> list[Trend]:
        return [self._current_trend, self._prevent_trend]
