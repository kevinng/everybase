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
            # Update user's current recommendation
            r = self.message.from_user.current_recommendation

            # Update recommendation choices
            r.recommend_details_choice = dv.value_string
            r.recommend_details_responded = now

            r.save()

        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__IMMEDIATE_CONFIRM,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__IMMEDIATE,
            params_func=lambda: {
                'is_buying': c.is_buying__current_recommendation()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__IMMEDIATE
        )

        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__CONTACT_US_AGAIN,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__NEED_TIME,
            params_func=lambda: {
                'is_buying': c.is_buying__current_recommendation(),
                'is_registered': c.is_registered()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__NEED_TIME
        )

        self.add_option([('3', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__NOT_INTERESTED,
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__DETAILS__NOT_INTERESTED
        )

        return self.reply_option()