import pytz, datetime
from relationships import models as relmods
from everybase.settings import TIME_ZONE
from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def run(self):
        self.save_body_as_string(datas.QUESTION)

        match = ContextLogic(self).get_match()
        if match is not None and match.closed is not None:
            return self.done_reply(intents.MENU, messages.MENU)

        # Create new QNA
        logic = ContextLogic(self)
        sgtz = pytz.timezone(TIME_ZONE)
        relmods.QuestionAnswerPair.objects.create(
            asked=datetime.datetime.now(tz=sgtz),
            questioner=self.message.from_user,
            answerer=logic.get_counter_party(),
            match=logic.get_match()
        )

        self.params['initial'] = True
        self.params['answering'] = False
        return self.done_reply(intents.QNA, messages.QNA__THANK_YOU)