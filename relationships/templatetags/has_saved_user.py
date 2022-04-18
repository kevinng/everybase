from relationships import models
from django import template

register = template.Library()

@register.simple_tag(name='has_saved_user')
def has_saved_user(saver, savee):
    if saver is None or saver == '' or savee is None or savee == '':
        return False

    try:
        saved_user = models.SavedUser.objects.get(
            saver=saver,
            savee=savee
        )
    except models.SavedUser.DoesNotExist:
        return False

    return saved_user.active