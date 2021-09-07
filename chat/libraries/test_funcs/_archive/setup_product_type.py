from relationships import models as relmods
from common import models as commods

def setup_product_type(
        name: str = None,
        uom_name: str = None,
        uom_plural_name: str = None,
        uom_description: str = None,
        keyword: str = 'Generic product keyword'
    ):
    """Set up product type, unit of measure and matching keyword

    Returns
    -------
    (product_type, unit_of_measure, keyword)
        product_type
            Product type model reference set up
        unit_of_measure
            Unit of measure model reference set up
        keyword
            Match keyword model reference set up
    """
    product_type = relmods.ProductType.objects.create(name=name)

    uom = relmods.UnitOfMeasure.objects.create(
        name=uom_name,
        plural_name=uom_plural_name,
        description=uom_description,
        product_type=product_type)

    # Create match keyword for test product type
    keyword = commods.MatchKeyword.objects.create(
        keyword=keyword,
        tolerance=0,
        product_type=product_type)

    return (product_type, uom, keyword)