from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='promoted_leads')
def promoted_leads():
    return models.Lead.objects.filter(
        is_promoted=True
    ).order_by('-created')