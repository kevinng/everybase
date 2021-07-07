import typing
from relationships import models as relmods
from common import models as commods
from chat.libraries.utilities.match import match

def get_product_type(match_string: str)\
    -> typing.Tuple[relmods.ProductType, relmods.UnitOfMeasure]:
    """Returns product type and its top UOM matching the input match string.
    """

    # Get all match keywords
    match_keywords = commods.MatchKeyword.objects.filter(
        product_type__isnull=False
    )

    # Match each keyword against user input
    product_type = None
    for k in match_keywords:
        if match(match_string, k.keyword, k.tolerance):
            # User input match a product type
            product_type = k.product_type

    uom = None
    if product_type is not None:
        # Matching product type found - get its top UOM
        try:
            uom = relmods.UnitOfMeasure.objects.filter(
                product_type=product_type
            ).order_by('-priority').first()
        except relmods.UnitOfMeasure.DoesNotExist:
            pass
    
    return (product_type, uom)