from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input without validation
        self.save_body_as_string(datas.\
            QNA__STOP_DISCUSSION__REASON__INPUT__STRING)
        return self.done_reply(
            intents.QNA,
            messages.STOP_DISCUSSION__THANK_YOU
        )