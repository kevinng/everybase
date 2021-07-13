from chat.libraries.constants import datas, intents
from chat.libraries.classes.message_handler import MessageHandler
from chat.tasks.save_new_supply import save_new_supply
from chat.tasks.save_new_supply_version import save_new_supply_version

class SupplyGetPriceReadyOTGKnownPackingHandler(MessageHandler):
    def run(self,
            next_intent_key: str,
            next_message_key: str
        ) -> str:
        self.save_body_as_string(datas.PRICE)

        # Trigger background task to save message
        if self.intent_key == intents.NEW_SUPPLY:
            save_new_supply.delay(self.message)
        elif self.intent_key == intents.DISCUSS_W_BUYER:
            save_new_supply_version.delay(self.message)
        
        return self.done_reply(next_intent_key, next_message_key)