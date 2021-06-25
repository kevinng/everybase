from relationships import models as relmods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler import MessageHandler

class Handler(MessageHandler):
    def _get_match_id(self):
        """Get the match ID set by the system when sending the last your-answer
        message to the user"""
        if not hasattr(self, '_match_id') or self._match_id is None:
            # Lazy, once-only, instantiation
            self._match_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_ANSWER,
                datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
                False
            ).value_id
        
        return self._match_id

    def _get_match(self):
        """Get match object reference from match ID"""
        if not hasattr(self, '_match') or self._match is None:
            # Lazy, once-only, instantiation
            self._match = relmods.Match.objects.get(pk=self._get_match_id())

        return self._match

    def _get_buying_boolean(self):
        """Returns True if match's buyer is this user, False otherwise."""
        match = self._get_match()
        if match.supply.user == self.message.from_user:
            # User is seller
            return False
        elif match.demand.user == self.message.from_user:
            # User is buyer
            return True

        return None

    def _get_qna_id(self):
        """Get last QNA ID"""
        if not hasattr(self, '_qna_id') or self._qna_id is None:
            self._qna_id = self.get_latest_value(
                intents.QNA,
                messages.YOUR_ANSWER,
                datas.QNA__YOUR_ANSWER__QNA_ID__ID,
                False
            ).value_id
        
        return self._qna_id

    def _get_qna(self):
        """Get QNA from QNA ID"""
        if not hasattr(self, '_qna') or self._qna is None:
            self._qna = relmods.QuestionAnswerPair.objects.get(
                pk=self._get_qna_id())

        return self._qna

    def _get_new_qna(self):
        """Get QNA initiated by this user that's created after the last one -
        there should be only 1 if it exists"""
        if not hasattr(self, '_new_qna') or self._new_qna is None:
            try:
                self._new_qna = relmods.QuestionAnswerPair.objects.filter(
                    match=self._get_match(),
                    created__gt=self._get_qna().created,
                    questioner=self.message.from_user
                ).order_by('-created').first()
            except relmods.QuestionAnswerPair.DoesNotExist:
                self._new_qna = None

        return self._new_qna

    def _has_asked_question(self):
        """Returns True if this user has initiated a new question after the
        last one"""
        return self._get_new_qna() is not None

    def _get_question_thank_you_params(self):
        """Get parameters for question/thank-you"""
        buying = self._get_buying_boolean()
        match = self._get_match()
        params = {
            # Show the NEW question initiated by the user back to him
            'question': \
                # Note: new QNA, not just QNA
                self._get_new_qna().question_captured_value.value_string,
            'buying': buying
        }

        if buying:
            params['supply'] = match.supply
        else:
            params['demand'] = match.demand

        return params

    def _get_your_answer_params(self):
        """Get parameters for your-answer"""
        qna = self._get_qna()

        if qna.use_auto_cleaned_question is not None and \
            qna.use_auto_cleaned_question:
            # Settings indicate use auto-cleaned question
            question = qna.auto_cleaned_question
        else:
            question = qna.manual_cleaned_question

        if qna.use_auto_cleaned_answer is not None and \
            qna.use_auto_cleaned_answer:
            # Settings indicate use auto-cleaned answer
            answer = qna.auto_cleaned_answer
        else:
            answer = qna.manual_cleaned_answer

        return {
            'name': self.message.from_user.name,
            'question': question,
            'answer': answer,
            'buying': self._get_buying_boolean()
        }

    def run(self):
        # Save stray input
        self.save_body_as_string(datas.\
            CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING)

        print('has asked question ' +str(self._has_asked_question()))

        if self._has_asked_question():
            return self.done_reply(
                intents.QNA,
                messages.QUESTION__THANK_YOU,
                self._get_question_thank_you_params()
            )

        return self.done_reply(
            intents.QNA,
            messages.YOUR_ANSWER,
            self._get_your_answer_params()
        )