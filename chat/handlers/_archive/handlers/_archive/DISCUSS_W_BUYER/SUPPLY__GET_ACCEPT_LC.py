from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.supply__get_accept_lc import \
    SupplyGetAcceptLCHandler

class Handler(SupplyGetAcceptLCHandler):
    def run(self):
        return super().run(intents.DISCUSS_W_BUYER, messages.DISCUSS__ASK)