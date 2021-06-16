from chat.libraries.message_handler import MessageHandler
from chat.libraries import intents, messages, datas

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING)

        return self.done_reply(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )