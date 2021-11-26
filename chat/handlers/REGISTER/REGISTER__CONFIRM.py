from chat.constants import intents, messages
from chat.utilities import render_message
from chat.handlers.library import MessageHandler

class Handler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            return self.done_reply(
                intents.REGISTER,
                messages.REGISTER__CONFIRMED)

        return render_message(messages.REGISTER__DO_NOT_UNDERSTAND, None)