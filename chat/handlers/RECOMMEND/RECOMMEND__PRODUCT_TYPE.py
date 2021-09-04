from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        c = ContextLogic(self)
        
        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__YES,
            params_func=lambda: {
                'buying': c.is_buying(),
                'lead_details': c.get_recommendation_lead_display_text()
            },
            amp_event_key=events.RECOMMEND__PRODUCT_TYPE__YES
        )
        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_NOW_CONFIRM,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__NOT_NOW,
            params_func=lambda: {
                'registered': c.is_registered()
            },
            amp_event_key=events.RECOMMEND__DETAILS__CAN_FIND
        )
        self.add_option([('3', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRM,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__NO,
            params_func=lambda: {
                'registered': c.is_registered()
            },
            amp_event_key=events.RECOMMEND__PRODUCT_TYPE__NO
        )

        return self.reply_option()