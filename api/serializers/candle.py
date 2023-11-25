from rest_framework import serializers

from api.models.candle import Candle


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = '__all__'
