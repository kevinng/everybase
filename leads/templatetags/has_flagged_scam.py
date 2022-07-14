from django import template
from leads import models

register = template.Library()

@register.simple_tag(name='has_flagged_scam')
def has_flagged_scam(request, lead):
    flag = None
    if not request.user.is_authenticated:
        try:
            cookie_uuid = request.COOKIES.get('uuid')
            if cookie_uuid is None:
                return False

            flag = models.LeadFlag.objects.get(
                lead=lead,
                cookie_uuid=cookie_uuid,
                type='scam'
            )
        except models.LeadFlag.DoesNotExist:
            return False
    else:
        found = False
        try:
            flag = models.LeadFlag.objects.get(
                lead=lead,
                user=request.user.user,
                type='scam'
            )
        except models.LeadFlag.DoesNotExist:
            found = False

        if not found:
            # TODO User may have logged in after flagging the lead, so the flag may be tied to the cookie UUID and not the user.
            pass

        
    return flag is not None