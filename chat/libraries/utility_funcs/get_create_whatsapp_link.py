from urllib.parse import urljoin
from django.urls import reverse
from relationships import models as relmods
from everybase import settings

def get_create_whatsapp_link(from_user, to_user, reverse_only=False) -> str:
    """Get/create WhatsApp URL for the to_user. Get/create phone
    number hash of WhatsApp-type for the from_user on the to_user and
    return a formatted WhatsApp URL."""
    whatsapp = relmods.PhoneNumberType.objects.get(id=1)

    hash, _ = relmods.PhoneNumberHash.objects.get_or_create(
        user=from_user,
        phone_number_type=whatsapp,
        phone_number=to_user.phone_number
    )

    reverse_url = reverse('chat_root:whatsapp', kwargs={ 'id': hash.id })

    if reverse_only:
        return reverse_url

    return urljoin(settings.BASE_URL, reverse_url)