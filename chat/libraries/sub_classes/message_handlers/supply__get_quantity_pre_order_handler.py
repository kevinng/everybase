from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetQuantityPreOrderHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUANTITY)
        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_PRICE_PRE_ORDER)