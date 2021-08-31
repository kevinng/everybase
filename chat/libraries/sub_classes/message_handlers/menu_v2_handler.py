from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.chosen_funcs.talk_to_an_everybase_human_agent import \
    talk_to_an_everybase_human_agent

class MenuHandler(MessageHandler):
    def run(self):
        registered = self.message.from_user.registered is not None

        self.add_option([('1', 0)],
            intents.FIND_ME_BUYERS,
            messages.FIND_BUYERS__GET_LEAD_LOCATION,
            datas.MENU,
            datas.MENU__FIND_ME_BUYERS,
            amp_event_key=events.CHOSE_FIND_ME_BUYERS
        )
        self.add_option([('2', 0)],
            intents.FIND_ME_SELLERS,
            messages.FIND_SELLERS__GET_LEAD_LOCATION,
            datas.MENU,
            datas.MENU__FIND_ME_SELLERS,
            amp_event_key=events.CHOSE_FIND_SELLERS_WITH_REPLY
        )
        # Don't run task functions in tests
        o3_chosen_func = None if self.no_task_calls else \
            talk_to_an_everybase_human_agent
        self.add_option([('3', 0)],
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN,
            datas.MENU,
            datas.MENU__TALK_TO_AN_EVERYBASE_AGENT,
            params_func=lambda : { 'registered': registered },
            chosen_func=o3_chosen_func,
            amp_event_key=events.CHOSE_TALK_TO_AN_EVERYBASE_HUMAN_AGENT
        )

        if not registered:
            # User is not registered, provide option to register
            self.add_option([('4', 0)],
                intents.REGISTER,
                messages.REGISTER__GET_NAME,
                datas.MENU,
                datas.MENU__REGISTER_ME,
                params_func=lambda : { 'registered': registered },
                amp_event_key=events.CHOSE_REGISTER_ME
            )

        return self.reply_option()