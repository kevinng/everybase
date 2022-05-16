from leads import models

def run():
    ffps = models.FilterFormPost.objects.all()

    for ffp in ffps:
        if (ffps.title == '' or ffps.title is None) and (ffps.details == '' or ffps.details is None):
            print('Delete ' + ffps)
            ffp.delete()