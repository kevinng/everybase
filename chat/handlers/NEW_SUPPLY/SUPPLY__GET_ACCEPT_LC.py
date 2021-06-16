from chat.libraries import intents, messages, datas
from chat.libraries.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU, None,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU, None,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO
        )
        return self.reply_option()