from rest_framework import serializers

from api.models.indicators import Sma, MaxMin, ParabolicSAR
from api.serializers import CandleSerializer


class SmaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma
        fields = '__all__'


class MaxMinListSerializer(serializers.ModelSerializer):
    candle = CandleSerializer()
    class Meta:
        model = MaxMin
        fields = '__all__'


class ParabolicSarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParabolicSAR
        fields = '__all__'