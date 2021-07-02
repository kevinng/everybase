import urllib.parse
from everybase.settings import BASE_URL

def get_payment_link(hash):
    return urllib.parse.urljoin(BASE_URL, str(hash.id))