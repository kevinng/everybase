from django.contrib import admin
from .models import (Incoterm, Currency)
from common.admin import ChoiceAdmin

admin.site.register(Incoterm, ChoiceAdmin)
admin.site.register(Currency, ChoiceAdmin)