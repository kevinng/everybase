from leads import models

def run():
    for f in models.FilterFormPost.objects.all():
        if (f.title is None or f.title == '') and (f.details is None or f.details == ''):
            print('Deleted ' + str(f))
            f.delete()