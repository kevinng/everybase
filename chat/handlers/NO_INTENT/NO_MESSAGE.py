from amplitude.constants import events
from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        if self.message.from_user.name is None:
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.done_reply(
                intents.REGISTER, messages.REGISTER__GET_NAME)

        self.send_event(events.ENTERED_FREE_TEXT)

        return self.done_reply(intents.MENU, messages.MENU)