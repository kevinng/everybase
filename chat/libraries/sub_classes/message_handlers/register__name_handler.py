from amplitude.constants import events
from chat.libraries.constants import messages
from chat.libraries.classes.message_handler import MessageHandler

class RegisterNameHandler(MessageHandler):
    def run(self):
        # Store message body as user's name
        user = self.message.from_user
        user.name = self.message.body.strip()
        user.save()

        self.send_event(events.ENTERED_FREE_TEXT)
        
        return self.done_reply(self.intent_key, messages.REGISTER__EMAIL)