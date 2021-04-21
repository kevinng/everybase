from django.contrib import admin

from . import models as mod
from common import admin as comadm

@admin.register(mod.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass