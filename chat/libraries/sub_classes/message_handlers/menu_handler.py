from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class MenuHandler(MessageHandler):
    def __init__(self, message, intent_key, message_key,
        invalid_option_data_key=datas.INVALID_CHOICE):
        super().__init__(message, intent_key, message_key)
        self._invalid_option_data_key = invalid_option_data_key

    def run(self):
        self.add_option([('1', 0), ('buyers', 1)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.MENU,
            datas.MENU__FIND_BUYERS)
        self.add_option([('2', 0), ('sellers', 1)],
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.MENU,
            datas.MENU__FIND_SELLERS)
        self.add_option([('3', 0)],
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE,
            datas.MENU,
            datas.MENU__LEARN_MORE)

        return self.reply_option(self._invalid_option_data_key)