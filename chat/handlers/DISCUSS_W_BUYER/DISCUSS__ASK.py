from chat.libraries import intents, messages, datas
from chat.libraries.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            DISCUSS_W_BUYER__DISCUSS__ASK__QUESTION__STRING)

        return self.done_reply(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__THANK_YOU
        )