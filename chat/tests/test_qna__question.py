from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class QNAQuestionTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.QUESTION)

    def _test_enter_answer(self, target_body_variation_key: str):
        input = 'Can you do OEM?'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QNA__THANK_YOU,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(
            datas.QUESTION,
            value_string=input
        )
        qna = self.user.current_qna
        self.assertNotEqual(qna.asked, None)
        self.assertNotEqual(qna.questioner, None)
        self.assertNotEqual(qna.answerer, None)
        self.assertNotEqual(qna.question_captured_value, None)
        self.assertNotEqual(qna.match, None)

class QNAQuestion_Buying_Test(QNAQuestionTest):
    def setUp(self):
        super().setUp()
        self.setup_match(True, SupplyAvailabilityOption.OTG)
        self.setup_qna(answered=True)

    def test_enter_question(self):
        self._test_enter_answer('QUESTIONING__BUYING__INITIAL')

class QNAQuestion_Selling_Test(QNAQuestionTest):
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        self.setup_qna(answered=True)

    def test_enter_question(self):
        self._test_enter_answer('QUESTIONING__SELLING__INITIAL')

class QNAQuestion_MatchClosed_Test(QNAQuestionTest):
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG, True)
        self.setup_qna()

    def test_stray_input(self):
        self.receive_reply_assert(
            'Yes, we can.',
            intents.MENU,
            messages.MENU
        )