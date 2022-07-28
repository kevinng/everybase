from leads import models

def run():
    print(models.Lead.objects.filter(author__first_name__isnull=True).count())