from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class DiscussAskHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUESTION)
        return self.done_reply(
            self.intent_key,
            messages.DISCUSS__THANK_YOU)