from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        c = ContextLogic(self)
        self.add_option([('1', 0)],
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRM,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__DIRECT,
            params_func=lambda: { 'registered': c.is_registered() },
            amp_event_key=events.RECOMMEND__DETAILS__DIRECT
        )
        self.add_option([('2', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__I_CAN_FIND,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__CAN_FIND,
            params_func=lambda: {
                'buying': c.is_current_recommendation_buying(),
                'registered': c.is_registered()
            },
            amp_event_key=events.RECOMMEND__DETAILS__CAN_FIND
        )
        self.add_option([('3', 0)],
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            datas.RECOMMEND__DETAILS,
            datas.RECOMMEND__DETAILS__NOT_INTERESTED,
            amp_event_key=events.RECOMMEND__DETAILS__NOT_INTERESTED
        )

        return self.reply_option()