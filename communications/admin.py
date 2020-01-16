from django.contrib import admin

from .models import Message, Recipient

admin.site.register(Message)
admin.site.register(Recipient)