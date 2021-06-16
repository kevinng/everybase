from chat.libraries import intents, messages, datas
from chat.libraries.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(
        datas.DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING)

        return self.done_reply(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_PRE_ORDER
        )