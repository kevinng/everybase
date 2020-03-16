from django.contrib import admin

from .models import (Company, UnitOfMeasure, Product, Agent, ProductsList,
    ProductsListAccessLogEntry, Lead, ProductsInterestsList)

class ProductInline(admin.StackedInline):
    model = Product
    extra = 20

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ('id', 'full_name', 'company')
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['full_name', 'quantity']}),
        ('Relationships', {'fields': ['uom', 'company']}),
    ]
    list_display = ('id', 'full_name', 'quantity', 'uom', 'company')

class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ('id', 'name')
    inlines = [ProductInline]
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['name']})
    ]
    list_display = ('id', 'name')

class AgentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ('id', 'first_name', 'last_name', 'email', 'whatsapp_no', 'wechat_no', 'wechat_id')
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['first_name', 'last_name', 'email', 'whatsapp_no', 'wechat_no', 'wechat_id']})
    ]
    list_display = ('id', 'first_name', 'last_name', 'email', 'whatsapp_no', 'wechat_no', 'wechat_id')

class ProductsListAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    search_fields = ('id', 'title')
    fieldsets = [
        (None, {'fields': ['id', 'title']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
        ('Relationships', {'fields': ['products', 'agent']})
    ]
    list_display = ('id', 'title', 'agent')

class ProductsListAccessLogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('accessed',)
    search_fields = ('ip_address', 'user_agent')
    fieldsets = [
        ('Timestamps', {'fields': ['accessed']}),
        ('Data', {'fields': ['ip_address', 'user_agent']}),
        ('Relationships', {'fields': ['products_list']}),
    ]
    list_display = ('accessed', 'ip_address', 'user_agent', 'products_list')

class LeadAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ('id', 'full_name', 'email')
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['full_name', 'email']})
    ]
    list_display = ('id', 'full_name', 'email')

class ProductsInterestsListAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'submitted')
    search_fields = ('id', 'products_list', 'lead')
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Timestamps', {'fields': ['submitted']}),
        ('Relationships', {'fields': ['products', 'products_list', 'lead']})
    ]
    list_display = ('submitted', 'id', 'products_list', 'lead')

class UnitOfMeasureAdmin(admin.ModelAdmin):
    search_fields = ('acronym', 'full_name')
    list_display = ('acronym', 'full_name')

admin.site.register(Company, CompanyAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(ProductsList, ProductsListAdmin)
admin.site.register(ProductsListAccessLogEntry, ProductsListAccessLogEntryAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(ProductsInterestsList, ProductsInterestsListAdmin)