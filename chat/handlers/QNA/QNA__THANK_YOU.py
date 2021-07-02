import pytz, datetime
from relationships import models as relmods
from everybase.settings import TIME_ZONE
from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.STRAY_INPUT)

        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        self.add_option([('1', 0)],
            intents.QNA,
            messages.QUESTION,
            datas.QNA,
            datas.QNA__ASK_QUESTION
        )
        self.add_option([('2', 0)],
            intents.QNA,
            messages.PLEASE_PAY,
            datas.QNA,
            datas.QNA__BUY_CONTACT
        )

        return self.reply_option()