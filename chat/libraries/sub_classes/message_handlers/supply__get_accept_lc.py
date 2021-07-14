from chat.libraries.constants import datas, intents
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic
from chat.tasks.save_new_supply import save_new_supply
from chat.tasks.save_new_supply_version import save_new_supply_version

class SupplyGetAcceptLCHandler(MessageHandler):
    def run(self,
            next_intent_key: str,
            next_message_key: str
        ) -> str:

        if self.intent_key == intents.NEW_SUPPLY:
            save_new_supply.delay(self.message.id)
        elif self.message_key == intents.DISCUSS_W_BUYER:
            logic = ContextLogic(self)
            save_new_supply_version.delay(logic.get_match().id, self.message.id)

        self.add_option([('1', 0), ('yes', 0)],
            next_intent_key,
            next_message_key,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__YES)
        self.add_option([('2', 0), ('no', 0)],
            next_intent_key,
            next_message_key,
            datas.ACCEPT_LC,
            datas.ACCEPT_LC__NO)

        return self.reply_option()