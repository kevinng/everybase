from relationships import models as relmods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_match_id(self):
        if not hasattr(self, '_match_id') or self._match_id is None:
            self._match_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_QUESTION,
                datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
                False
            ).value_id
        
        return self._match_id

    def _get_match(self):
        if not hasattr(self, '_match') or self._match is None:
            self._match = relmods.Match.objects.get(pk=self._get_match_id())

        return self._match

    def _get_buying_boolean(self):
        match = self._get_match()
        if match.supply.user == self.message.from_user:
            # User is seller
            return False
        elif match.demand.user == self.message.from_user:
            # User is buyer
            return True

        return None

    def _get_qna_id(self):
        if not hasattr(self, '_qna_id') or self._qna_id is None:
            self._qna_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_QUESTION,
                datas.QNA__YOUR_QUESTION__QNA_ID__ID,
                False
            ).value_id
        
        return self._qna_id

    def _get_qna(self):
        if not hasattr(self, '_qna') or self._qna is None:
            self._qna = relmods.QuestionAnswerPair.objects.get(
                pk=self._get_qna_id())

        return self._qna

    def _is_answered(self):
        return self._get_qna().answered is not None

    def _get_qna_in_progress_params(self):
        buying = self._get_buying_boolean()
        match = self._get_match()
        params = {
            'buying': buying
        }

        if buying:
            params['supply'] = match.supply
        else:
            params['demand'] = match.demand

        return params

    def _get_your_question_params(self):
        qna = self._get_qna()
        if qna.use_auto_cleaned_question is not None and \
            qna.use_auto_cleaned_question:
            question = qna.auto_cleaned_question
        else:
            question = qna.manual_cleaned_question

        return {
            'name': self.message.from_user.name,
            'question': question,
            'buying': self._get_buying_boolean()
        }

    def run(self):
        # Save stray input
        self.save_body_as_string(datas.\
            CONNECT__PLEASE_PAY__STRAY_INPUT__STRING)

        if self._is_answered():
            return self.done_reply(
                intents.QNA,
                messages.QNA__IN_PROGRESS,
                self._get_qna_in_progress_params()
            )

        return self.done_reply(
            intents.QNA,
            messages.YOUR_QUESTION,
            self._get_your_question_params()
        )