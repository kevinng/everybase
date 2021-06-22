from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class MenuHandler(MessageHandler):
    def __init__(self, message, intent_key, message_key,
        invalid_option_data_key=None):
        super().__init__(message, intent_key, message_key)
        self._invalid_option_data_key = invalid_option_data_key

    def run(self):
        self.add_option([('1', 0), ('find buyers', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )
        self.add_option([('2', 0), ('find sellers', 3)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_SELLER
        )
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE, None,
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__LEARN_MORE
        )
        return self.reply_option(self._invalid_option_data_key)