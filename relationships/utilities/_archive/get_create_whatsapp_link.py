from urllib.parse import urljoin
from django.urls import reverse
from relationships import models as relmods
from everybase import settings

def get_create_whatsapp_link(
        from_user : relmods.User,
        to_user : relmods.User,
        reverse_only : bool = False
    ) -> str:
    """Get/create WhatsApp URL from from_user to to_user. Idempotent.

    Parameters
    ----------
    from_user
        User contacting.
    to_user
        User contacted.
    reverse_only
        If True, return Django-reversed-looked-up URL only, without the base
        URL. I.e., a relative URL is returned. Otherwise, an absolute URL
        with the base URL will be returned.
    
    Returns
    -------
    url
        Cloaked WhatsApp URL from from_user to to_user.
    """
    whatsapp = relmods.PhoneNumberType.objects.get(id=1)

    hash, _ = relmods.PhoneNumberHash.objects.get_or_create(
        user=from_user,
        phone_number_type=whatsapp,
        phone_number=to_user.phone_number
    )

    reverse_url = reverse('whatsapp', kwargs={ 'id': hash.id })

    if reverse_only:
        return reverse_url

    return urljoin(settings.BASE_URL, reverse_url)