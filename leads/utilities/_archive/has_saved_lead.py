from leads import models as lemods

def has_saved_lead(user, lead):
    return lemods.SavedLead.objects.filter(
        saver=user,
        lead=lead
    ).count() > 0