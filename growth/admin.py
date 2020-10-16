from django.contrib import admin
from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail)
from common.admin import (standard_list_display, standard_list_filter,
    standard_ordering, standard_readonly_fields, standard_fieldsets,
    standard_list_editable)

admin.site.register(GmassCampaignResult)
admin.site.register(GmassCampaign)
admin.site.register(Fibre2FashionResult)
admin.site.register(ZeroBounceResult)
admin.site.register(DataSource)
admin.site.register(SourcedEmail)

@admin.register(ChemicalClusterOfSingaporeResult)
class ChemicalClusterOfSingaporeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_editable = standard_list_editable + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_per_page = 1000
    list_filter = standard_list_filter + ['sourced']
    search_fields = ['id', 'company_name', 'telephone', 'fax', 'website',
        'source_link']
    ordering = standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Source', {'fields': ['sourced', 'source_link']}),
        ('Result details', {
            'fields': ['company_name', 'telephone', 'fax', 'email_str', 'website',
                'address_str']
        }),
        ('Model references', {
            'fields': ['company', 'email', 'phone_numbers', 'link', 'address']
        })
    ]
    autocomplete_fields = ['company', 'email', 'phone_numbers', 'link',
        'address']