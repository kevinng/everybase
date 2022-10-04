from leads import models
from relationships import models as relmods
from django.db.models import Q
from relationships.utilities.get_or_set_cookie_uuid import get_or_create_cookie_uuid

def has_flagged_lead(request, lead, type):
    user = request.user.user if request.user.is_authenticated else None
    cookie_uuid, _ = get_or_create_cookie_uuid(request)

    associated_cookie_uuids = relmods.LoginAction.objects.filter(user=user).values_list('cookie_uuid', flat=True)

    flag = models.LeadFlag.objects.filter(
        lead=lead,
        type=type,
        deleted__isnull=True
    ).filter(Q(user=user) | Q(cookie_uuid=cookie_uuid) | Q(cookie_uuid__in=associated_cookie_uuids))\
    .order_by('-updated').first()

    return flag is not None