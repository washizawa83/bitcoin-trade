from django.urls import path

from api.views.candle import CandlesView
from api.views.indicators import SmaListView, MaxMinListView, ParaboricSarListView
from api.views.settings import SettingView


urlpatterns = [
    path('candles/', CandlesView.as_view(), name='candles'),
    path('smas/', SmaListView.as_view(), name='sma'),
    path('maxmins/', MaxMinListView.as_view(), name='maxmin'),
    path('parabolicSars/', ParaboricSarListView.as_view(), name='parabolicSAR'),
    path('settings/<str:pk>', SettingView.as_view(), name='settings'),
]