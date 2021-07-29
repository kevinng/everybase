from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class MenuHandler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('buyers', 1)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.MENU,
            datas.MENU__FIND_BUYERS,
            amp_event_key=events.CHOSE_FIND_BUYERS_WITH_REPLY
        )
        self.add_option([('2', 0), ('sellers', 1)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.MENU,
            datas.MENU__FIND_SELLERS,
            amp_event_key=events.CHOSE_FIND_SELLERS_WITH_REPLY
        )
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE,
            datas.MENU,
            datas.MENU__LEARN_MORE,
            amp_event_key=events.CHOSE_LEARN_MORE_WITH_REPLY
        )

        return self.reply_option()