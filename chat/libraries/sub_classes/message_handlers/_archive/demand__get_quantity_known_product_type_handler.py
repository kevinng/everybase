from amplitude.constants import events
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class DemandGetQuantityKnownProductTypeHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUANTITY)
        self.send_event(events.ENTERED_FREE_TEXT)
        
        return self.done_reply(
            self.intent_key,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE)