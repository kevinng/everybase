from leads import models

def get_application_messages(pk):
    application = models.Application.objects.get(pk=pk)
    return models.ApplicationMessage.objects\
        .filter(application=application)\
        .order_by('-created')