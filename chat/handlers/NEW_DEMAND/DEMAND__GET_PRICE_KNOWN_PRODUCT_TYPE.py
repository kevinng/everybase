from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.\
    demand__get_price_known_product_type import \
    DemandGetPriceKnownProductTypeHandler

class Handler(DemandGetPriceKnownProductTypeHandler):
    def run(self):
        return super().run(intents.NEW_DEMAND, messages.DEMAND__THANK_YOU)