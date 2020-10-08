from django.contrib import admin
from .models import Incoterm
from common.admin import ChoiceAdmin

admin.site.register(Incoterm, ChoiceAdmin)