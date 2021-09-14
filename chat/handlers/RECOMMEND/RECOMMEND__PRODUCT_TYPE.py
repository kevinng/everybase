import pytz, datetime
from everybase.settings import TIME_ZONE
from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        c = ContextLogic(self)

        sgtz = pytz.timezone(TIME_ZONE)
        now = datetime.datetime.now(tz=sgtz)

        def chosen_func(self, dv):
            r = self.message.from_user.current_recommendation
            r.recommend_product_type_choice = dv.value_string
            r.recommend_product_type_responded = now
            r.save()
        
        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__YES,
            params_func=lambda: {
                'buying': c.is_current_recommendation_buying(),
                'lead_details': c.get_recommendation_lead_display_text()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__PRODUCT_TYPE__YES
        )
        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_NOW_CONFIRMED,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__NOT_NOW,
            params_func=lambda: {
                'registered': c.is_registered()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__CAN_FIND
        )
        self.add_option([('3', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRMED,
            datas.RECOMMEND__PRODUCT_TYPE,
            datas.RECOMMEND__PRODUCT_TYPE__NO,
            params_func=lambda: {
                'registered': c.is_registered()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__PRODUCT_TYPE__NO
        )

        return self.reply_option()