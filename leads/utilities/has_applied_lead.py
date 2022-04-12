from leads import models as lemods

def has_applied_lead(user, lead):
    return lemods.Application.objects.filter(
        lead=lead,
        applicant=user
    ).count() > 0