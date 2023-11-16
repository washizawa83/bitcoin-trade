import datetime

from django.conf import settings
import pybitflyer


class ApiClient:
    def __init__(self) -> None:
        self._api = pybitflyer.API(
            api_key=settings.BIT_FLYER_API_KEY,
            api_secret=settings.BIT_FLYER_API_SECRET
        )

    def fetch_ticker(self):
        try:
            return self._api.ticker()
        except:
            print('Error fetch_ticker function is class ApiClient')

    def get_balance(self, mid_price: float):
        try:
            balance = self._api.getbalance()
        except:
            print('Error get_balance function is class ApiClient')
            return
        jpy = balance[0]['amount']
        btc = balance[1]['amount']
        delta = int(mid_price * btc)
        total = jpy + delta
        return jpy, btc, total, delta

    def buy_order(self):
        try:
            order = self._api.sendchildorder(
                product_code='BTC_JPY',
                child_order_type='MARKET',
                side='BUY',
                size=0.001,
                minute_to_expire=10000,
                time_in_force='GTC'
            )
            return order
        except:
            print('Error buy_order function is class ApiClient')
            return

    def sell_order(self):
        try:
            order = self._api.sendchildorder(
                product_code='BTC_JPY',
                child_order_type='MARKET',
                side='SELL',
                size=0.001,
                minute_to_expire=10000,
                time_in_force='GTC'
            )
            return order
        except:
            print('Error sell_order function is class ApiClient')
            return

    def order_histories(self) -> list:
        side_status = {'BUY': '買い', 'SELL': '売り'}
        order_status = {'COMPLETED': '取引済み', 'CANCELED': 'キャンセル',
                        'EXPIRED': '有効期限切れ', 'REJECTED': '取引失敗'}
        try:
            histories_data = self._api.getchildorders()
        except:
            print('Error order_histories function is class ApiClient')
            return
        histories = []
        for history in histories_data:
            # TODO 要動作確認
            date = datetime.datetime.timestamp(history['child_order_date']) + datetime.timedelta(hours=9)
            side = side_status[history['side']]
            status = order_status[history['child_order_state']]
            histories.append([date, side, history['size'],
                             history['average_price'], status])
        return histories
