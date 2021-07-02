from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.STOP_DISCUSSION__REASON)

        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        return self.done_reply(intents.QNA, messages.STOP_DISCUSSION__THANK_YOU)