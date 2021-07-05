from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class DemandGetQuantityUnknownProductTypeHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUANTITY)
        return self.done_reply(
            self.intent_key,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE)