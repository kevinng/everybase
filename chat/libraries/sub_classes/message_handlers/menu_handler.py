from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.chosen_funcs.talk_to_an_everybase_human_agent import \
    talk_to_an_everybase_human_agent
from chat.libraries.classes.context_logic import ContextLogic

class MenuHandler(MessageHandler):
    def run(self):
        c = ContextLogic(self)
        
        self.add_option([('1', 0)],
            intents.FIND_BUYERS,
            # Register first if not registered
            messages.GET_LEAD__LOCATION if c.is_registered() else \
                messages.REGISTER__NAME,
            datas.MENU,
            datas.MENU__FIND_BUYERS,
            params_func=\
                lambda: { 'buying': False } if c.is_registered() else None,
            amp_event_key=events.MENU__FIND_BUYERS
        )
        self.add_option([('2', 0)],
            intents.FIND_SELLERS,
            # Register first if not registered
            messages.GET_LEAD__LOCATION if c.is_registered() else \
                messages.REGISTER__NAME,
            datas.MENU,
            datas.MENU__FIND_SELLERS,
            params_func=lambda: { 'buying': True },
            amp_event_key=events.MENU__FIND_SELLERS
        )
        self.add_option([('3', 0)],
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRMED,
            datas.MENU,
            datas.MENU__TALK_TO_AN_EVERYBASE_AGENT,
            params_func=lambda : { 'registered': c.is_registered() },
            # Don't run tasks in tests
            chosen_func=None if self.no_task_calls else \
                talk_to_an_everybase_human_agent,
            amp_event_key=events.MENU__TALK_TO_AN_EVERYBASE_AGENT
        )

        if not c.is_registered():
            # User is not registered, provide option to register
            self.add_option([('4', 0)],
                intents.REGISTER,
                messages.REGISTER__NAME,
                datas.MENU,
                datas.MENU__REGISTER_ME,
                params_func=lambda : { 'registered': c.is_registered() },
                amp_event_key=events.MENU__REGISTER_ME
            )

        return self.reply_option()