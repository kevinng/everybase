from relationships import models as relmods
from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        user = relmods.User.objects.get(pk=self.message.from_user.id)
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})