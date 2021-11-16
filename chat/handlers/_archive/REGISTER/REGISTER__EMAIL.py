from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.register__email_handler \
    import RegisterEmailHandler

class Handler(RegisterEmailHandler):
    def run(self):
        return super().run(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU,
            lambda : { 'is_registered': ContextLogic(self).is_registered() }
        )