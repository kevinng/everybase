from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, \
    SupplyAvailabilityOption

class QNAQuestionTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.QUESTION)
        self.setup_buyer(SupplyAvailabilityOption.OTG)
        self.setup_qna(answered=True)

    def test_enter_question(self):
        input = 'Can you do OEM?'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QUESTION__THANK_YOU
        )
        self.assert_value(
            datas.QUESTION,
            value_string=input
        )
        qna = self.user.current_qna
        self.assertNotEqual(qna.asked, None)
        self.assertNotEqual(qna.answerer, None)
        self.assertNotEqual(qna.questioner, None)