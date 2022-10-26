from relationships import models

def run():
    models.User.objects.filter(id__gt=3).delete()