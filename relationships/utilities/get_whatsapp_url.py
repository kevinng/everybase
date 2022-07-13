import urllib

def get_whatsapp_url(
        country_code: str,
        national_number: str,
        text: str=None
    ) -> str:
    """Returns WhatsApp URL for phone number and text body.

    Parameters
    ----------
    country_code
        Country code of the phone number.
    national_number
        National number of the phone number.
    text
        WhatsApp body text to attach to the link.
    """
    url = 'https://wa.me/' + country_code + national_number
    if text is not None:
        url = url + '?text=' + urllib.parse.quote(text)
    return url