import pytz, datetime
from everybase.settings import TIME_ZONE

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            self.save_body_as_string(datas.INVALID_CHOICE)
            return self.done_reply(intents.MENU, messages.MENU)

        def update_match(message_handler, data_value):
            """Updates match - stop discussion"""
            logic = ContextLogic(message_handler)
            sgtz = pytz.timezone(TIME_ZONE)
            match = logic.get_match()
            
            # Update match
            if logic.is_buying():
                match.buyer_stopped_discussion = datetime.datetime.now(sgtz)
                match.buyer_stopped_discussion_value = data_value
            else:
                match.seller_stopped_discussion = datetime.datetime.now(sgtz)
                match.seller_stopped_discussion_value = data_value
            match.save()

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
            datas.QNA__STOP_DISCUSSION,
            chosen_func=update_match)

        return self.reply_option()