import pytz, datetime

from everybase.settings import TIME_ZONE
from relationships import models as relmods
from common import models as commods
from payments import models as paymods

from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption, SupplyAvailabilityOptions
from chat.libraries.test_funcs.setup_product_type import setup_product_type

def setup_match(
    buying: bool,
    supply_type: SupplyAvailabilityOptions,
    user_1: relmods.User,
    user_2: relmods.User,
    closed: bool = False
) -> relmods.Match:
    """Set up a user_1 as either a buyer or a seller, and user_2 as the
    counter-party (i.e., seller if user is buyer, vice versa).

    Parameters
    ----------
    buying
        If true, set up user as the buyer, otherwise - set him up as the
        seller.
    supply_type
        The type of supply either the user/user_2 is selling - depending
        on who's the buyer.
    user_1
        User for whom we're setting this match up for
    user_2
        Counter-party to user_1. E.g., seller if user_1 is buyer.
    closed
        Close the match immediately.
    """

    # Product type and packing for both supply and demand
    product_type, packing, _ = setup_product_type(
        name='Nitrile Gloves',
        uom_name='Box',
        uom_plural_name='Boxes',
        uom_description='200 pieces in 1 box'
    )

    # Supply availability
    if supply_type == SupplyAvailabilityOption.OTG:
        availability = relmods.Availability.objects.get(pk=1)
    elif supply_type == SupplyAvailabilityOption.PRE_ORDER_DEADLINE or \
        supply_type == SupplyAvailabilityOption.PRE_ORDER_DURATION:
        availability = relmods.Availability.objects.get(pk=2)

    # Supply timeframe
    pre_order_timeframe = None
    sgtz = pytz.timezone(TIME_ZONE)
    if supply_type == SupplyAvailabilityOption.PRE_ORDER_DEADLINE:
        pre_order_timeframe = relmods.TimeFrame.objects.create(
            deadline=datetime.datetime(2021, 2, 5, tzinfo=sgtz))
    elif supply_type == SupplyAvailabilityOption.PRE_ORDER_DURATION:
        pre_order_timeframe = relmods.TimeFrame.objects.create(
            duration_uom='d',
            duration=5
        )

    # Supply
    supply = relmods.Supply.objects.create(
        user=user_1 if not buying else user_2,
        product_type=product_type,
        packing=packing,
        country=commods.Country.objects.get(pk=601), # Israel
        availability=availability,
        pre_order_timeframe=pre_order_timeframe,
        quantity=12000,
        price=15.15,
        currency=paymods.Currency.objects.get(pk=1), # USD
        deposit_percentage=0.4,
        accept_lc=False
    )

    # Demand
    demand = relmods.Demand.objects.create(
        user=user_1 if buying else user_2,
        product_type=product_type,
        packing=packing,
        country=commods.Country.objects.get(pk=601), # Israel
        quantity=12000,
        price=15.15,
        currency=paymods.Currency.objects.get(pk=1) # USD
    )

    # Set up and return match
    return relmods.Match.objects.create(
        supply=supply,
        demand=demand,
        closed=datetime.datetime.now(tz=pytz.timezone(TIME_ZONE)) \
            if closed else None
    )