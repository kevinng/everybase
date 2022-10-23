


# from leads import models as lemods

# class LeadInlineAdmin(admin.TabularInline):
#     model = lemods.Lead
#     extra = 0
#     fields = ['lead_link']
#     readonly_fields = ['lead_link']

#     def lead_link(self, obj):
#         link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
#         link += f'/leads/lead/{obj.id}/change'
#         return format_html(
#             f'<a href="{link}" target="{link}">{obj.headline}</a>')

# class ApplicationMessageInlineAdmin(admin.TabularInline):
#     model = lemods.ApplicationMessage
#     extra = 0
#     fields = ['application_link', 'body', 'applicant_link', 'lead_author_link']
#     readonly_fields = ['application_link', 'body', 'applicant_link', 'lead_author_link']

#     def application_link(self, obj):
#         link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
#         link += f'/leads/application/{obj.application.id}/change'
#         return format_html(f'<a href="{link}" target="{link}">{obj.application}</a>')
    
#     def applicant_link(self, obj):
#         link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
#         link += f'/relationships/user/{obj.application.applicant.id}/change'
#         return format_html(f'<a href="{link}" target="{link}">{obj.application.applicant.first_name} {obj.application.applicant.last_name}</a>')

#     def lead_author_link(self, obj):
#         link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
#         link += f'/relationships/user/{obj.application.lead.author.id}/change'
#         return format_html(f'<a href="{link}" target="{link}">{obj.application.lead.author.first_name} {obj.application.lead.author.last_name}</a>')

# _user_comment_fields = ['commentee', 'commentor', 'body']
# @admin.register(models.UserComment)
# class UserCommentAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _user_comment_fields
#     list_editable = comadm.standard_list_editable + _user_comment_fields
#     search_fields = comadm.standard_search_fields + ['commentee__first_name',
#         'commentee__last_name', 'commentor__first_name', 'commentor__last_name',
#         'body']

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': _user_comment_fields})
#     ]
#     autocomplete_fields = ['commentee', 'commentor']

# _login_token_fields = ['user', 'activated', 'killed','token']
# @admin.register(models.LoginToken)
# class LoginTokenAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _login_token_fields
#     list_editable = comadm.standard_list_editable + _login_token_fields
#     list_filter = comadm.standard_list_filter + ['created']
#     search_fields = comadm.standard_search_fields + ['token']

#     # Details page settings
#     readonly_fields = comadm.standard_readonly_fields + ['created']
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': _login_token_fields})
#     ]
#     autocomplete_fields = ['user']

# _register_token_fields = ['user', 'activated', 'killed', 'token']
# @admin.register(models.RegisterToken)
# class RegisterTokenAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _register_token_fields
#     list_editable = comadm.standard_list_editable + _register_token_fields
#     list_filter = comadm.standard_list_filter + ['created']
#     search_fields = comadm.standard_search_fields + ['user__first_name',
#         'user__last_name', 'token']

#     # Details page settings
#     readonly_fields = comadm.standard_readonly_fields + ['created']
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': _register_token_fields})
#     ]
#     autocomplete_fields = ['user']



# _saved_user_fields = ['active', 'saver', 'savee']
# @admin.register(models.SavedUser)
# class SavedUserAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _saved_user_fields
#     list_editable = comadm.standard_list_editable + _saved_user_fields
#     list_filter = comadm.standard_list_filter + ['active']
#     search_fields = comadm.standard_search_fields + ['saver__id',
#         'saver__family_first_name', 'saver__family_last_name', 'savee__id',
#         'savee__family_first_name', 'savee__family_last_name',]

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _saved_user_fields})]
#     autocomplete_fields = ['saver', 'savee']

# _user_query_fields = ['user', 'commented_only', 'saved_only', 'connected_only',
# 'first_name', 'last_name', 'company_name', 'country', 'goods_string',
# 'languages', 'is_buy_agent', 'buy_agent_details', 'is_sell_agent',
# 'sell_agent_details', 'is_logistics_agent', 'logistics_agent_details']
# @admin.register(models.UserQuery)
# class UserQueryAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _user_query_fields
#     list_editable = comadm.standard_list_editable + _user_query_fields
#     search_fields = comadm.standard_search_fields + ['user__id',
#         'commented_only', 'saved_only', 'connected_only', 'first_name',
#         'last_name', 'company_name', 'country', 'goods_string', 'languages',
#         'is_buy_agent', 'buy_agent_details', 'is_sell_agent',
#         'sell_agent_details', 'is_logistics_agent', 'logistics_agent_details']

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _user_query_fields})]
#     autocomplete_fields = ['user']

# _magic_login_redirect_fields = ['uuid', 'next']
# @admin.register(models.MagicLinkRedirect)
# class MagicLoginRedirectAdmin(comadm.StandardAdmin):
#     list_display = comadm.standard_list_display + _magic_login_redirect_fields
#     list_editable = [] # Speed up loading
#     search_fields = comadm.standard_search_fields + _magic_login_redirect_fields

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': _magic_login_redirect_fields})
#     ]