import urllib

def get_non_tracking_whatsapp_link(
        country_code : str,
        national_number : str,
        text : str = None
    ):
    """Get non-tracking WhatsApp link. If a tracking (cloaked) link is required,
    use the get_create_whatsapp_link function instead.

    Parameters
    ----------
    country_code
        Country code of the contactee.
    national_number
        National number of the contactee.
    text
        WhatsApp body text to attach to the link.

    Returns
    -------
    url
        WhatsApp URL.
    """
    url = 'https://wa.me/' + country_code + national_number
    if text is not None:
        url = url + '?' + urllib.parse.quote(text)
    return url