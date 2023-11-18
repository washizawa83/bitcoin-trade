from django.contrib import admin
from trade.models.candle import Candle

from trade.models.settings import Settings


admin.site.register(Settings)
admin.site.register(Candle)