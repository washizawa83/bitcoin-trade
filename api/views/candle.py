from django.shortcuts import render
from rest_framework import generics

from api.models.candle import Candle
from api.serializers.candle import CandleSerializer


class CandleView(generics.ListApiView):
    queryset = Candle.objects.all()
    serializer = CandleSerializer()