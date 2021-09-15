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
            r.recommend_immediate_confirm_choice = dv.value_string
            r.recommend_immediate_confirm_responded = now

            r.save()

        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            datas.RECOMMEND__IMMEDIATE_CONFIRM,
            datas.RECOMMEND__IMMEDIATE_CONFIRM__YES,
            params_func=lambda: {
                'is_registered': c.is_registered()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__IMMEDIATE_CONFIRM__YES
        )
        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            datas.RECOMMEND__IMMEDIATE_CONFIRM,
            datas.RECOMMEND__IMMEDIATE_CONFIRM__CANCEL,
            params_func=lambda: {
                'is_buying': c.is_buying__current_recommendation(),
                'lead_details': c.get_recommendation_lead_display_text()
            },
            chosen_func=chosen_func,
            amp_event_key=events.RECOMMEND__IMMEDIATE_CONFIRM__CANCEL
        )
        
        return self.reply_option()