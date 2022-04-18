from django import template

register = template.Library()

@register.simple_tag(name='string_equal')
def string_equal(one, two):
    return str(one) == str(two)