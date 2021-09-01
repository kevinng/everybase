from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.STRAY_INPUT)
        self.send_event(events.ENTERED_STRAY_TEXT)
        return self.done_reply(intents.MENU, messages.MENU)