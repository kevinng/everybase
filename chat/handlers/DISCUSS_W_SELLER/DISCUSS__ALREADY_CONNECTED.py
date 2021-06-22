from relationships import models as relmods
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(
    datas.DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED__INVALID_CHOICE__STRING)
        user = relmods.User.objects.get(pk=self.message.from_user.id)
        return self.done_reply(intents.MENU, messages.MENU, {'name': user.name})