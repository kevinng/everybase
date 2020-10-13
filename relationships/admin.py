from django.contrib import admin
from .models import (PersonLinkType, PersonLink)

admin.site.register(PersonLinkType)
admin.site.register(PersonLink)