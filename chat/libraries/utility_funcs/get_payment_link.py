from urllib.parse import urljoin
from django.urls import reverse
from everybase.settings import BASE_URL

def get_payment_link(hash):
    return urljoin(BASE_URL,
        reverse('chat_root:payment', kwargs={ 'id': hash.id }))