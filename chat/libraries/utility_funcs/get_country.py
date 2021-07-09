from common import models as commods
from chat.libraries.utility_funcs.match import match

def get_country(match_string: str)\
    -> commods.Country:
    """Returns Country matching the input match string."""

    # Get all match keywords
    match_keywords = commods.MatchKeyword.objects.filter(
        country__isnull=False
    )

    # Match each keyword against user input
    country = None
    for k in match_keywords:
        if match(match_string, k.keyword, k.tolerance):
            # User input match a product type
            country = k.country

    return country