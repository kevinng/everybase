from amplitude.constants import events
from chat.libraries.constants import datas, messages
from chat.libraries.classes.message_handler import MessageHandler

class GetLeadLocationHandler(MessageHandler):
    def run(self, buying):
        self.save_body_as_string(datas.LOCATION)
        self.send_event(events.ENTERED_FREE_TEXT)
        return self.done_reply(
            self.intent_key,
            messages.GET_LEAD__DETAILS,
            params_func=lambda : { 'buying': buying }
        )