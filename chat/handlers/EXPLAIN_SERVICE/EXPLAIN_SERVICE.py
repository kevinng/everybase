from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('find buyers', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT, None,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_BUYER
        )
        self.add_option([('2', 0), ('find sellers', 3)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT, None,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_SELLER
        )
        self.add_option([('3', 0)],
            intents.SPEAK_HUMAN,
            messages.CONFIRM_HUMAN, None,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__SPEAK_HUMAN
        )
        return self.reply_option()