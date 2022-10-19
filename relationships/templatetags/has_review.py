from django import template
from relationships import models

register = template.Library()

@register.simple_tag(name='has_review')
def has_review(phone_number, reviewer=None):
    if reviewer is not None:
        return models.Review.objects.filter(
            reviewer=reviewer,
            phone_number=phone_number
        ).count() > 0
    else:
        return models.Review.objects.filter(
            phone_number=phone_number
        ).count() > 0