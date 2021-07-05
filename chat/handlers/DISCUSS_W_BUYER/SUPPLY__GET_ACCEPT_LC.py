from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__YES)
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__NO)
            
        return self.reply_option()