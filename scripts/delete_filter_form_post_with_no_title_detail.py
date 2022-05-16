from leads import models

def run():
    models.FilterFormPost.objects.filter(
        title='',
        details=''
    ).delete()