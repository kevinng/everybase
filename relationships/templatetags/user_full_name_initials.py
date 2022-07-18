from django import template

register = template.Library()

@register.simple_tag(name='user_full_name_initials')
def user_full_name_initials(user):
    if (user.first_name is None or user.first_name.strip() == '') or\
        (user.last_name is None or user.last_name.strip() == ''):
        return None
    
    return f'{user.first_name[0].capitalize()}{user.last_name[0].capitalize()}'