from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.\
    supply__get_price_ready_otg_known_packing import \
    SupplyGetPriceReadyOTGHandler

class Handler(SupplyGetPriceReadyOTGHandler):
    def run(self):
        return super().run(intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)