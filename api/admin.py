from django.contrib import admin

from api.models.auth import Auth
from api.models.settings import Settings
from api.models.candle import Candle
from api.models.indicators import Sma, MaxMin, ParabolicSAR


admin.site.register(Auth)
admin.site.register(Settings)
admin.site.register(Candle)
admin.site.register(Sma)
admin.site.register(MaxMin)
admin.site.register(ParabolicSAR)