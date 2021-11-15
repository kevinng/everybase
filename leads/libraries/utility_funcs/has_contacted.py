from leads import models as lemods

def has_contacted(user, lead):
    return lemods.ContactRequest.objects.filter(
        contactor=user,
        lead=lead
    ).count() > 0