from pyexpat import model
from leads import models

def get_application_count(lead):
    return models.Application.objects.filter(
        lead=lead
    ).count()