import urllib

def get_non_tracking_whatsapp_link(country_code, national_number, text=None):
    url = 'https://wa.me/' + country_code + national_number
    if text is not None:
        url = url + '?' + urllib.parse.quote(text)
    return url