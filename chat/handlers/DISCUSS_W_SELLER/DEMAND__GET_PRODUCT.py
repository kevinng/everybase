from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING)

        return self.done_reply(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE
        )