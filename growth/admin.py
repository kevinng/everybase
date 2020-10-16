from django.contrib import admin
from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail)
from common.admin import (standard_list_display, standard_list_filter,
    standard_ordering, standard_readonly_fields, standard_fieldsets,
    standard_list_editable)

admin.site.register(GmassCampaignResult)
admin.site.register(GmassCampaign)
admin.site.register(ChemicalClusterOfSingaporeResult)
admin.site.register(Fibre2FashionResult)
admin.site.register(ZeroBounceResult)
admin.site.register(DataSource)
admin.site.register(SourcedEmail)


class ConversationChatAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['status', 'our_number',
        'their_number', 'conversation']
    list_editable = standard_list_editable + ['status', 'our_number',
        'their_number', 'conversation'] 
    list_per_page = 1000
    list_filter = standard_list_filter + ['status']
    search_fields = ['id', 'their_number', 'our_number', 'conversation']
    ordering = standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Basic Details', {'fields': ['status']}),
        ('Phone Numbers', {
            'fields': ['their_number', 'our_number'],
            'description': 'Phone numbers involved in this chat conversation'
        }),
        ('Conversation', {
            'fields': ['conversation'],
            'description': 'Base conversation'
        })
    ]
    autocomplete_fields = ['status', 'their_number', 'our_number',
        'conversation']