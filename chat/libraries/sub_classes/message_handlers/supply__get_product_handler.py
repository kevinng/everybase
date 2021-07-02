from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetProductHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.PRODUCT)
        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_AVAILABILITY)