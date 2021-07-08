from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.chosen_funcs.update_match__stopped_discussion \
    import update_match__stopped_discussion

class Handler(MessageHandler):
    def run(self):
        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        self.add_option([('1', 0)],
            intents.QNA,
            messages.ANSWER,
            datas.QNA,
            datas.QNA__ANSWER_QUESTION
        )
        self.add_option([('2', 0)],
            intents.QNA,
            messages.PLEASE_PAY,
            datas.QNA,
            datas.QNA__BUY_CONTACT
        )
        self.add_option([('3', 0)],
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            datas.QNA,
            datas.QNA__STOP_DISCUSSION,
            chosen_func=update_match__stopped_discussion
        )

        return self.reply_option()