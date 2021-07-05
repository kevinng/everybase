from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class DemandGetQuantityKnownProductTypeHandler(MessageHandler):
    def run(self):
        if self.save_body_as_string(datas.QUANTITY) is None:
            return self.reply_invalid_numeric_value()
        
        return self.done_reply(
            self.intent_key,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE)