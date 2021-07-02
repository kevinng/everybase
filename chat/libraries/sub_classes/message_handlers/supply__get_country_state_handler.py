from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class SupplyGetCountryStateHandler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.COUNTRY_STATE)

        if ContextLogic(self).is_known_packing():
            return self.done_reply(
                self.intent_key,
                messages.SUPPLY__CONFIRM_PACKING)

        return self.done_reply(
            self.intent_key,
            messages.SUPPLY__GET_PACKING)