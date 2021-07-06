from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, SupplyAvailabilityOption

class QNAAnswerTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.ANSWER)

    def _test_enter_answer(self, target_body_variation_key: str):
        input = 'Yes, we can.'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QNA__THANK_YOU,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(datas.ANSWER, value_string=input)
        qna = self.user.current_qna
        self.assertNotEqual(qna.answered, None)
        self.assertNotEqual(qna.answerer, None)
        self.assertNotEqual(qna.questioner, None)

class QNAAnswer_Buying_Test(QNAAnswerTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(True, SupplyAvailabilityOption.OTG)
        self.setup_qna()

    def test_enter_answer(self):
        self._test_enter_answer('ANSWERING__BUYING__INITIAL')

class QNAAnswer_Selling_Test(QNAAnswerTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(False, SupplyAvailabilityOption.OTG)
        self.setup_qna()

    def test_enter_answer(self):
        self._test_enter_answer('ANSWERING__SELLING__INITIAL')

class QNAAnswer_MatchClosed_Test(QNAAnswerTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(False, SupplyAvailabilityOption.OTG, True)
        self.setup_qna()

    def test_enter_answer(self):
        self.receive_reply_assert(
            'Yes, we can.',
            intents.MENU,
            messages.MENU
        )
