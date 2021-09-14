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
            r.recommend_details_choice = dv.value_string
            r.recommend_details_responded = now
            r.save()

        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__DIRECT,
            params_func=lambda: { 'is_registered': c.is_registered() },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__DIRECT
        )

        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__I_CAN_FIND,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__CAN_FIND,
            params_func=lambda: {
                'is_buying': c.is_buying__current_recommendation(),
                'is_registered': c.is_registered()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__CAN_FIND
        )

        self.add_option([('3', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_NOW_CONFIRMED,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__NOT_NOW,
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__NOT_NOW
        )

        self.add_option([('4', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__NOT_INTERESTED,
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__NOT_INTERESTED
        )

        return self.reply_option()