import typing
from enum import Enum

class SupplyAvailabilityOption(Enum):
    OTG = 1
    PRE_ORDER_DEADLINE = 2
    PRE_ORDER_DURATION = 3

SupplyAvailabilityOptions = typing.NewType(
    'SupplyAvailabilityOptions', SupplyAvailabilityOption)