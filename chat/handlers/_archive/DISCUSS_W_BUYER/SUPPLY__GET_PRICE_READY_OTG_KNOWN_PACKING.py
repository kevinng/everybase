from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.\
    supply__get_price_ready_otg_known_packing import \
    SupplyGetPriceReadyOTGKnownPackingHandler

class Handler(SupplyGetPriceReadyOTGKnownPackingHandler):
    def run(self):
        return super().run(intents.DISCUSS_W_BUYER, messages.DISCUSS__ASK)