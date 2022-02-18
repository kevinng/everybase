import pytz
from django.db.models import Q
from datetime import datetime
from everybase import settings
from relationships import models

def kill_login_tokens(user, exclude_id=None):
    live_tokens = models.LoginToken.objects.filter(user=user)\
        .filter(
            Q(is_not_latest__isnull=True) | # Is latest
            Q(activated__isnull=True) | # Not activated
            Q(killed__isnull=True) # Not killed
        )

    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz=sgtz)
    for t in live_tokens:
        if exclude_id is not None and t.id != exclude_id:
            t.killed = now
            t.is_not_latest = True
            t.save()