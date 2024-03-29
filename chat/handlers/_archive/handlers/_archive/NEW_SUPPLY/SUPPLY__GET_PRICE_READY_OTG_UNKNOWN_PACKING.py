from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.\
    supply__get_price_ready_otg_unknown_packing import \
    SupplyGetPriceReadyOTGUnknownPackingHandler

class Handler(SupplyGetPriceReadyOTGUnknownPackingHandler):
    def run(self):
        return super().run(intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)