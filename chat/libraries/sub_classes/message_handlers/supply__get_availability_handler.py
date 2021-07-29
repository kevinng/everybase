from amplitude.constants import events
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class SupplyGetAvailabilityHandler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('otg', 0), ('ready', 1)],
            self.intent_key,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG,
            amp_event_key=events.CHOSE_READY_STOCK_OTG_WITH_REPLY
        )
        self.add_option([('2', 0), ('pre order', 3)],
            self.intent_key,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            datas.AVAILABILITY,
            datas.AVAILABILITY__PRE_ORDER,
            amp_event_key=events.CHOSE_PRE_ORDER_WITH_REPLY
        )
            
        return self.reply_option()