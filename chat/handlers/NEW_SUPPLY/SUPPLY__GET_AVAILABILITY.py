from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.add_option([('1', 0), ('otg', 0), ('ready', 1)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            None,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )
        self.add_option([('2', 0), ('pre order', 3)],
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            None,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )
        return self.reply_option()