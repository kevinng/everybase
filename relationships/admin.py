from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompanyType)

admin.site.register(PersonLinkType)
admin.site.register(PersonLink)
admin.site.register(PersonCompanyType)