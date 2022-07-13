from django import template
from leads import models

register = template.Library()

@register.simple_tag(name='has_flagged_spam')
def has_flagged_spam(request, lead):
    flag = None
    if not request.user.is_authenticated:
        try:
            cookie_uuid = request.COOKIES.get('uuid')
            if cookie_uuid is None:
                return False

            flag = models.LeadFlag.objects.get(
                lead=lead,
                cookie_uuid=cookie_uuid,
                type='spam'
            )
        except models.LeadFlag.DoesNotExist:
            return False
    else:
        try:
            flag = models.LeadFlag.objects.get(
                lead=lead,
                user=request.user.user,
                type='spam'
            )
        except models.LeadFlag.DoesNotExist:
            return False
        
    return flag is not None