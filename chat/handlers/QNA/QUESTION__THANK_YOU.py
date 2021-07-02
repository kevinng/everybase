from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        self.add_option([('1', 0)],
            intents.QNA,
            messages.QUESTION,
            datas.QNA,
            datas.QNA__ASK_QUESTION)
        self.add_option([('2', 0)],
            intents.QNA,
            messages.PLEASE_PAY,
            datas.QNA,
            datas.QNA__BUY_CONTACT)
        self.add_option([('3', 0)],
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            datas.QNA,
            datas.QNA__LEARN_MORE)

        return self.reply_option()