from django import template
from relationships import models

register = template.Library()

@register.simple_tag(name='has_review')
def has_review(user, phone_number):
    return models.Review.objects.filter(
        reviewer=user,
        phone_number=phone_number
    ).count() > 1