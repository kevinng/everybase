from leads import models as lemods

def has_applied_lead(user, lead):
    if user is None or user == '' or lead is None or lead == '':
        return False

    return lemods.Application.objects.filter(
        lead=lead,
        applicant=user
    ).count() > 0