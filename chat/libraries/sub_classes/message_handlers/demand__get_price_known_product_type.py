from chat.libraries.constants import datas, intents
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic
from chat.tasks.save_new_demand import save_new_demand
from chat.tasks.save_new_demand_version import save_new_demand_version

class DemandGetPriceKnownProductTypeHandler(MessageHandler):
    def run(self,
            next_intent_key: str,
            next_message_key: str
        ) -> str:
        self.save_body_as_string(datas.PRICE)

        if self.intent_key == intents.NEW_DEMAND:
            save_new_demand.delay(self.message.id)
        elif self.message_key == intents.DISCUSS_W_SELLER:
            logic = ContextLogic(self)
            save_new_demand_version.delay(logic.get_match().id, self.message.id)

        return self.done_reply(
            next_intent_key,
            next_message_key
        )