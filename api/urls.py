from django.urls import path

from api.views.candle import CandlesView



urlpatterns = [
    path('candles/', CandlesView.as_view(), name='candles'),
]