from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod)
from common.admin import ChoiceAdmin, ParentChildrenChoice

admin.site.register(Incoterm, ChoiceAdmin)
admin.site.register(Currency, ChoiceAdmin)
admin.site.register(PaymentMode, ChoiceAdmin)
admin.site.register(ContactType, ChoiceAdmin)
admin.site.register(LeadCategory, ParentChildrenChoice)
admin.site.register(MatchMethod, ChoiceAdmin)