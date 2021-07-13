from chat.models import TwilioInboundMessage
from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages, datas, methods
from chat.libraries.utility_funcs.get_product_type import get_product_type
from chat.libraries.utility_funcs.get_country import get_country
from chat.libraries.utility_funcs.get_value_string import get_value_string

@shared_task
def save_new_demand(
        last_message_id: int,
        new_version: bool = False
    ) -> relmods.Demand:
    """Save new demand entered by the user. Triggered at the end of the 'new
    demand's sequence.

    Parameters
    ----------
    last_message_id
        ID of the last TwilioInboundMessage of the 'new supply' sequence.
    new_version
        If True, use intent key for saving a copy of this demand.
    """
    last_message = TwilioInboundMessage.objects.get(pk=last_message_id)

    # The intent key determines if we're creating a new demand or creating a
    # new version of an old one
    intent_key = intents.DISCUSS_W_SELLER if new_version else intents.NEW_DEMAND

    user = last_message.from_user
    demand = relmods.Demand.objects.create(user=user)

    # Short-form for get_value_string with preset parameters
    gvs = lambda i, m, d, n: get_value_string(i, m, d, user, last_message, n)

    # Product type and packing UOM
    product_str, product_val = gvs(
        intent_key,
        messages.DEMAND__GET_PRODUCT,
        datas.PRODUCT,
        'Product type'
    )

    product_type, uom = get_product_type(product_str)

    demand.product_type_data_value = product_val
    demand.product_type_method = methods.FREE_TEXT_INPUT
    demand.product_type = product_type

    # Convenience function ascertain if product type is found
    ptype_found = lambda: product_type is not None and uom is not None

    # Country
    country_str, country_val = gvs(
        intent_key,
        messages.DEMAND__GET_COUNTRY_STATE,
        datas.COUNTRY_STATE,
        'Country'
    )
    demand.country_data_value = country_val
    demand.country_method = methods.FREE_TEXT_INPUT
    demand.country = get_country(country_str) # May be none if not set up

    # Quantity
    if ptype_found():
        quantity_msg_key = messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
    else:
        quantity_msg_key = messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE

    _, quantity_val = gvs(
        intent_key,
        quantity_msg_key,
        datas.QUANTITY,
        'Quantity'
    )

    demand.quantity_data_value = quantity_val
    demand.quantity_method = methods.FREE_TEXT_INPUT

    # Price
    if ptype_found():
        price_msg = messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
    else:
        price_msg = messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE

    _, price_val = gvs(
        intent_key,
        price_msg,
        datas.PRICE,
        'Price'
    )
    demand.price_data_value = price_val
    demand.price_method = methods.FREE_TEXT_INPUT

    demand.save()

    return demand