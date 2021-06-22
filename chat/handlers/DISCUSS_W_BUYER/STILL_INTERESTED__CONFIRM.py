from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_BUYER,
            messages.STILL_INTERESTED__THANK_YOU, None,
            datas.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__CHOICE,
            datas.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_BUYER,
            messages.STILL_INTERESTED__THANK_YOU, None,
            datas.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__CHOICE,
            datas.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__NO
        )
        return self.reply_option(
    datas.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM__INVALID_CHOICE__STRING)