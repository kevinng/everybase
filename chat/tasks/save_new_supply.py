from chat.models import TwilioInboundMessage
from celery import shared_task
from relationships import models as relmods
from chat.libraries.constants import intents, messages, datas, methods
from chat.libraries.utility_funcs.get_product_type import get_product_type
from chat.libraries.utility_funcs.get_country import get_country
from chat.libraries.utility_funcs.get_value_string import get_value_string
from chat.libraries.utility_funcs.get_value_float import get_value_float

@shared_task
def save_new_supply(
        last_message: TwilioInboundMessage,
        new_version: bool = False
    ) -> relmods.Supply:
    """Save new supply entered by the user. Triggered at the end of the 'new
    supply's sequence.

    Parameters
    ----------
    last_message
        Last TwilioInboundMessage of the 'new supply' sequence

    Returns
    -------
    Supply created
    """
    # The intent key determines if we're creating a new supply or creating a
    # new version of an old one
    intent_key = intents.DISCUSS_W_BUYER if new_version else intents.NEW_SUPPLY

    user = last_message.from_user
    supply = relmods.Supply.objects.create(user=user)

    # Short-form for get_value_string/float with preset parameters
    gvs = lambda i, m, d, n: get_value_string(i, m, d, user, last_message, n)
    gvf = lambda i, m, d, n: get_value_float(i, m, d, user, last_message, n)

    # Product type and packing UOM
    product_str, product_val = gvs(
        intent_key,
        messages.SUPPLY__GET_PRODUCT,
        datas.PRODUCT,
        'Product'
    )
    product_type, uom = get_product_type(product_str)
    supply.product_type_data_value = product_val
    supply.product_type_method = methods.FREE_TEXT_INPUT
    supply.product_type = product_type

    # Convenience function ascertain if product type is found
    ptype_found = lambda: product_type is not None and uom is not None

    # Availability
    availability_str, availability_val = gvs(
        intent_key,
        messages.SUPPLY__GET_AVAILABILITY,
        datas.AVAILABILITY,
        'Availability'
    )

    # Convenience function to return the right value on availability string
    def a_paths(
            ready_otg_known_val,
            ready_otg_unknown_val,
            pre_order_val
        ):
        if availability_str == datas.AVAILABILITY__READY_OTG:
            if product_type is not None and uom is not None:
                return ready_otg_known_val
            else:
                return ready_otg_unknown_val
        elif availability_str == datas.AVAILABILITY__PRE_ORDER:
            return pre_order_val

    # Update supply's availability
    supply.availability_data_value = availability_val
    supply.availability_method = methods.DATA_KEY_MATCH
    supply.availability = relmods.Availability.objects.get(
        pk=a_paths(1, 1, 2))

    # Country
    country_str, country_val = gvs(
        intent_key,
        a_paths(
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        ),
        datas.COUNTRY_STATE,
        'Country'
    )
    supply.country_data_value = country_val
    supply.country_method = methods.FREE_TEXT_INPUT
    supply.country = get_country(country_str) # May be none if not set up

    # Confirm packing
    if ptype_found():
        cfm_pack_str, cfm_pack_val = gvs(
            intent_key,
            messages.SUPPLY__CONFIRM_PACKING,
            datas.CONFIRM_PACKING,
            'Confirm packing'
        )
        if cfm_pack_str == datas.CONFIRM_PACKING__YES:
            # User confirms packing is correct
            supply.packing_data_value = cfm_pack_val
            supply.packing_method = methods.DATA_KEY_MATCH
            supply.packing = uom
    
    # Packing description
    if not ptype_found() or cfm_pack_str == datas.CONFIRM_PACKING__NO:
        # Product-type is not found or user confirms packing is wrong
        _, pack_desc_val = gvs(
            intent_key,
            messages.SUPPLY__GET_PACKING,
            datas.PACKING,
            'Packing description'
        )
        supply.packing_data_value = pack_desc_val
        supply.packing_method = methods.FREE_TEXT_INPUT

    # Quantity
    _, quantity_val = gvs(
        intent_key,
        a_paths(
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        ),
        datas.QUANTITY,
        'Quantity'
    )
    supply.quantity_data_value = quantity_val
    supply.quantity_method = methods.FREE_TEXT_INPUT

    # Price
    _, price_val = gvs(
        intent_key,
            a_paths(
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING,
            messages.SUPPLY__GET_PRICE_PRE_ORDER
        ),
        datas.PRICE,
        'Price'
    )
    supply.price_data_value = price_val
    supply.price_method = methods.FREE_TEXT_INPUT

    # Deposit and accept-LC
    # Only if availability is pre-order
    if availability_str == datas.AVAILABILITY__PRE_ORDER:
        deposit_flt, deposit_val = gvf(
            intent_key,
            messages.SUPPLY__GET_DEPOSIT,
            datas.DEPOSIT,
            'Deposit'
        )
        accept_lc_str, accept_lc_val = gvs(
            intent_key,
            messages.SUPPLY__GET_ACCEPT_LC,
            datas.ACCEPT_LC,
            'Accept LC'
        )
        supply.deposit_percentage = deposit_flt
        supply.deposit_percentage_data_value = deposit_val
        supply.deposit_percentage_method = methods.NUMERIC_INPUT
        supply.accept_lc_data_value = accept_lc_val
        supply.accept_lc_method = methods.DATA_KEY_MATCH
        supply.accept_lc = accept_lc_str == datas.ACCEPT_LC__YES
    
    supply.save()

    return supply