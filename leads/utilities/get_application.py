from leads import models

def get_application(applicant, lead):
    return models.Application.objects.filter(
        lead=lead,
        applicant=applicant
    ).first()