from enum import auto
import pytz, datetime
from everybase.settings import TIME_ZONE
from relationships import models as relmods
from chat.libraries.constants import messages, datas
from chat.libraries.classes.message_handler import MessageHandler
from chat.libraries.classes.context_logic import ContextLogic
from chat.tasks.auto_clean_question import auto_clean_question

class DiscussAskHandler(MessageHandler):
    def run(self):
        value = self.save_body_as_string(datas.QUESTION)

        logic = ContextLogic(self)
        sgtz = pytz.timezone(TIME_ZONE)
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.message.from_user,
            answerer=logic.get_counter_party(),
            asked=datetime.datetime.now(tz=sgtz),
            question_captured_value=value,
            match=logic.get_match()
        )

        auto_clean_question.delay(qna.id)

        return self.done_reply(
            self.intent_key,
            messages.DISCUSS__THANK_YOU
        )