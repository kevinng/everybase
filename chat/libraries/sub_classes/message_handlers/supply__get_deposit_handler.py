from amplitude.constants import events
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetDepositHandler(MessageHandler):
    def run(self):
        if self.save_body_as_float(datas.DEPOSIT) is None:
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.reply_invalid_numeric_value()

        self.send_event(events.ENTERED_FREE_TEXT)
        
        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_ACCEPT_LC)