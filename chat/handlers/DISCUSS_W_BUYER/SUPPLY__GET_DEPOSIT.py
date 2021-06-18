from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        # Save user input, deposit is None if value cannot be converted from
        # string to float
        deposit = self.save_body_as_float(
            datas.DISCUSS_W_BUYER__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER)

        if deposit is None:
            # User input is invalid
            return self.reply_invalid_number()
        
        return self.done_reply(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_ACCEPT_LC
        )