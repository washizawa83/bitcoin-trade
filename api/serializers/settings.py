from rest_framework import serializers

from api.models.settings import Settings


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
