from typing import TYPE_CHECKING, Tuple
from chat import models
from chat.libraries.utility_funcs.get_latest_value import get_latest_value
import sentry_sdk

if TYPE_CHECKING:
    from relationships import models as relmods

def get_value_float(
        intent_key: str,
        message_key: str,
        data_key: str,
        user: 'relmods.User',
        before_message,
        value_name
    ) -> Tuple[float, models.MessageDataValue]:
    value = get_latest_value(
        intent_key,
        message_key,
        data_key,
        user,
        before_message
    )

    value_flt = 0
    if value is None:
        sentry_sdk.capture_message('%s not found' % value_name, 'fatal')
    else:
        value_flt = value.value_float
    
    return (value_flt, value)
