from django.contrib import admin

from .models import Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'created', 'i_want_to',
        'chat_app', 'whatsapp_no', 'wechat_no')
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'name', 'email', 'ip_address']}),
        ('Chat', {'fields': ['chat_app', 'whatsapp_no', 'wechat_no']}),
        ('Role', {'fields': ['i_want_to', 'i_am_interested_to_buy']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]
    list_filter = ['created', 'i_want_to']
    search_fields = ['name', 'email', 'i_am_interested_to_buy',
        'whatsapp_no', 'wechat_no']

admin.site.register(Lead, LeadAdmin)