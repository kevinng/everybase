from django.contrib import admin

from .models import (Account, Organization, AccountOrganization,
    EmailVerificationCode, PasswordResetCode, OrganizationInvitationCode)

class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'user', 'active_organization']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
    ]

class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'name']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
    ]

class AccountOrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    fieldsets = [
        (None, {'fields': ['role', 'account', 'organization']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]

class EmailVerificationCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created')
    fieldsets = [
        (None, {'fields': ['id', 'email', 'verified', 'ip_address']}),
        ('Timestamps', {'fields': ['created']})
    ]

class PasswordResetCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created')
    fieldsets = [
        (None, {'fields': ['id', 'account', 'used']}),
        ('Timestamps', {'fields': ['created']})
    ]

class OrganizationInvitationCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created')
    fieldsets = [
        (None, {'fields': ['id', 'email', 'used']}),
        ('Timestamps', {'fields': ['created']})
    ]

admin.site.register(Account, AccountAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(AccountOrganization, AccountOrganizationAdmin)
admin.site.register(EmailVerificationCode, EmailVerificationCodeAdmin)
admin.site.register(PasswordResetCode, PasswordResetCodeAdmin)
admin.site.register(OrganizationInvitationCode, OrganizationInvitationCodeAdmin)