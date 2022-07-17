from django import template

register = template.Library()

@register.simple_tag(name='has_incomplete_profile')
def has_incomplete_profile(user):
    """Returns None if user's profile is complete. Otherwise, return dictionary with field name as key, and boolean as value to indicate if field is NOT set."""
    n = lambda x : x is not None or (type(x) == str and x.strip() != '')
    return {
        'first_name': n(user.first_name),
        'last_name': n(user.last_name),
        'country': n(user.country),
        'email': n(user.email),
        'phone_number': n(user.phone_number)
    }