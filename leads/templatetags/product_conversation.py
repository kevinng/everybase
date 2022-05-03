from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='product_conversation')
def product_conversation(product, user):
    """Returns the conversation the user has for this product,
    if it exists, or None if it does not."""
    return models.Application.objects.filter(
        lead=product,
        applicant=user,
        deleted__isnull=True
    ).first()