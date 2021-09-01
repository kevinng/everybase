from chat.libraries.constants import messages
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):

        # self.save_body_as_string(datas.COUNTRY_STATE)

        # self.send_event(events.ENTERED_FREE_TEXT)

        # if ContextLogic(self).is_known_packing():
        #     return self.done_reply(
        #         self.intent_key,
        #         messages.SUPPLY__CONFIRM_PACKING,
        #     )

        return self.done_reply(self.intent_key, messages.GET_LEAD__DETAILS)