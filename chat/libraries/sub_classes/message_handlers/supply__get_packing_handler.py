from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class SupplyGetPackingHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.PACKING)

        logic = ContextLogic(self)
        if logic.is_ready_otg():
            if logic.is_known_packing():
                return self.done_reply(
                    self.intent_key,
                    messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING)
            else:
                return self.done_reply(
                    self.intent_key,
                    messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING)
        elif logic.is_pre_order():
            return self.done_reply(
                self.intent_key,
                messages.SUPPLY__GET_QUANTITY_PRE_ORDER)
        
        return None