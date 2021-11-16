from chat.libraries.constants import intents, messages
from chat.libraries.utility_funcs.render_message import render_message
from chat.libraries.classes.message_handler import MessageHandler

class RegisterConfirmHandler(MessageHandler):
    def run(self):
        if self.message.body.strip().lower() == 'yes':
            return self.done_reply(
                intents.CONTACT_REQUEST,
                messages.CONTACT_REQUEST__THANK_YOU)

        return render_message(messages.CONTACT_REQUEST__CONFIRM_BAD, None)