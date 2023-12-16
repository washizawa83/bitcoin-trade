from django.shortcuts import render
from rest_framework import generics

from api.models.indicators import Sma, MaxMin, ParabolicSAR
from api.serializers.indicators import SmaListSerializer, MaxMinListSerializer, ParabolicSarListSerializer


class SmaListView(generics.ListAPIView):
    queryset = Sma.objects.all()
    serializer_class = SmaListSerializer


class MaxMinListView(generics.ListAPIView):
    queryset = MaxMin.objects.prefetch_related('candle').all()
    serializer_class = MaxMinListSerializer


class ParaboricSarListView(generics.ListAPIView):
    queryset = ParabolicSAR.objects.all()
    serializer_class = ParabolicSarListSerializer