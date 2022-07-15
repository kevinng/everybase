from leads import models

def has_flagged_lead(request, lead, type):
    if request.user.is_authenticated:
        # Look for scam flags with this user/lead.
        try:
            flag = models.LeadFlag.objects.get(
                lead=lead,
                user=request.user.user,
                type=type
            )
            return flag is not None
        except models.LeadFlag.DoesNotExist:
            pass
        
        # User may have logged in after flagging, so we look for scam flags with this user's lead/cookie-UUID.
        cookie_uuid = request.COOKIES.get('uuid')
        if cookie_uuid is None:
            return False

        try:
            flag = models.LeadFlag.objects.get(
                lead=lead,
                cookie_uuid=cookie_uuid,
                type=type
            )
            return flag is not None
        except models.LeadFlag.DoesNotExist:
            pass

        return False
    else:
        cookie_uuid = request.COOKIES.get('uuid')
        if cookie_uuid is None:
            # Unable to get cookie UUID, so there's no way to ascertain if this user has flagged the lead.
            return False

        try:
            flag = models.LeadFlag.objects.get(
                lead=lead,
                cookie_uuid=cookie_uuid,
                type=type
            )
            return flag is not None
        except models.LeadFlag.DoesNotExist:
            pass

        return False