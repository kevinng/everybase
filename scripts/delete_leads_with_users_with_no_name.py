from leads import models

def run():
    print(models.Lead.objects.filter(author__first_name__isnull=True).count())
    print(models.Lead.objects.filter(author__last_name__isnull=True).count())
    print(models.Lead.objects.filter(author__first_name__isnull=True).filter(author__last_name__isnull=True).count())