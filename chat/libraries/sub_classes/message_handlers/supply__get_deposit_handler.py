from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetDepositHandler(MessageHandler):
    def run(self):
        if self.save_body_as_float(datas.DEPOSIT) is None:
            return self.reply_invalid_numeric_value()
        
        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_ACCEPT_LC)