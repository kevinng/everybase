import pytz, datetime
from everybase.settings import TIME_ZONE
from amplitude.constants import events
from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        r = self.message.from_user.current_recommendation
        r.recommend_details_not_interested_text = self.message.body.strip()
        sgtz = pytz.timezone(TIME_ZONE)
        r.recommend_details_not_interested_responded = \
            datetime.datetime.now(tz=sgtz)
        r.save()

        self.send_event(events.ENTERED_FREE_TEXT)

        return self.done_reply(
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRM,
            lambda : { 'registered': ContextLogic(self).is_registered() }
        )