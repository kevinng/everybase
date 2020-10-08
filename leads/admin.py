from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType)
from common.admin import ChoiceAdmin

admin.site.register(Incoterm, ChoiceAdmin)
admin.site.register(Currency, ChoiceAdmin)
admin.site.register(PaymentMode, ChoiceAdmin)
admin.site.register(ContactType, ChoiceAdmin)