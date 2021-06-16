from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_discuss_ask_params(self):
        return {'buying': True}

    def run(self):
        self.add_option([('1', 0), ('yes', 0)],
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ASK, self._get_discuss_ask_params,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__YES
        )
        self.add_option([('2', 0), ('no', 0)],
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE, None,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS__NO
        )
        return self.reply_option()