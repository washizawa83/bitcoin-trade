from django.shortcuts import render
from rest_framework import generics

from api.models.settings import Settings
from api.serializers.settings import SettingSerializer


class SettingView(generics.RetrieveUpdateAPIView):
    queryset = Settings.objects.first()
    serializer_class = SettingSerializer
    lookup_field = 'pk'