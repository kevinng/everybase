from leads import models as lemods

def has_contacted(user, lead):
    if isinstance(user, str):
        # User is not authenticated
        return False

    return lemods.ContactRequest.objects.filter(
        contactor=user,
        lead=lead
    ).count() > 0