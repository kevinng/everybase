from chat.constants import intents, messages
from chat.utilities.render_message import render_message
from chat.handlers.library import MessageHandler

class Handler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            return self.done_reply(
                intents.LOGIN,
                messages.LOGIN__CONFIRMED)

        return render_message(messages.LOGIN__DO_NOT_UNDERSTAND, None)