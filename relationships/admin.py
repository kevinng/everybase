from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompanyType,
    PersonAddressType, PersonAddress)

admin.site.register(PersonLinkType)
admin.site.register(PersonLink)
admin.site.register(PersonCompanyType)
admin.site.register(PersonAddressType)
admin.site.register(PersonAddress)