from amplitude.constants import events
from chat.libraries.constants import intents, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic
from chat.tasks.save_new_supply import save_new_supply
from chat.tasks.save_new_supply_version import save_new_supply_version

class SupplyGetPriceReadyOTGUnknownPackingHandler(MessageHandler):
    def run(self,
            next_intent_key: str,
            next_message_key: str
        ) -> str:
        self.save_body_as_string(datas.PRICE)

        self.send_event(events.ENTERED_FREE_TEXT)

        # Trigger background task to save message
        if self.intent_key == intents.NEW_SUPPLY:
            if self.no_task_calls is False:
                save_new_supply.delay(self.message.id)
        elif self.intent_key == intents.DISCUSS_W_BUYER:
            logic = ContextLogic(self)
            if self.no_task_calls is False:
                save_new_supply_version.delay(logic.get_match().id, self.message.id)

        return self.done_reply(
            next_intent_key,
            next_message_key
        )