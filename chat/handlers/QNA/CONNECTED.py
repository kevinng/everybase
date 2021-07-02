from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.STRAY_INPUT)
        return self.done_reply(intents.MENU, messages.MENU)