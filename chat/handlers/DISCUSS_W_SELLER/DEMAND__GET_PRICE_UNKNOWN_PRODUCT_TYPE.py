from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.\
    demand__get_price_unknown_product_type import \
    DemandGetPriceUnknownProductTypeHandler

class Handler(DemandGetPriceUnknownProductTypeHandler):
    def run(self):
        return super().run(intents.DISCUSS_W_SELLER, messages.DISCUSS__ASK)