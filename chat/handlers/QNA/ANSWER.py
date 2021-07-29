import pytz, datetime
from everybase.settings import TIME_ZONE
from amplitude.constants import events
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.ANSWER)

        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            self.send_event(events.ENTERED_STRAY_TEXT)
            return self.done_reply(intents.MENU, messages.MENU)

        self.send_event(events.ENTERED_FREE_TEXT)

        # Update QNA
        logic = ContextLogic(self)
        sgtz = pytz.timezone(TIME_ZONE)
        qna = logic.get_qna()
        qna.answered = datetime.datetime.now(tz=sgtz)
        qna.save()

        self.params['initial'] = True

        return self.done_reply(intents.QNA, messages.QNA__THANK_YOU)