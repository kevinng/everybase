from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        if self.message.from_user.name is None:
            return self.done_reply(
                intents.REGISTER, messages.REGISTER__GET_NAME)

        return self.done_reply(intents.MENU, messages.MENU)