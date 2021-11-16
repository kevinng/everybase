from chat.libraries.constants import intents, messages
from chat.libraries.sub_classes.message_handlers.register__email_handler \
    import RegisterEmailHandler

class Handler(RegisterEmailHandler):
    def run(self):
        return super().run(
            intents.FIND_BUYERS,
            messages.GET_LEAD__LOCATION,
            lambda : { 'is_buying': False }
        )