from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetQuantityReadyOTGUnknownPackingHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUANTITY)
        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING)