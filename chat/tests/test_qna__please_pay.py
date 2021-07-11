from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class QNAPleasePayTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.PLEASE_PAY)

    def _test_stray_input(
            self,
            intent_key: str,
            message_key: str,
            target_body_variation_key: str = None
        ):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intent_key,
            message_key,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(
            datas.STRAY_INPUT,
            value_string=input
        )

class QNAPleasePay_AnsweredNoFollowUpQuestion_Buying_Test(QNAPleasePayTest):
    """User is buying, answered seller's question, not followed up with a
    question to the seller."""

    def setUp(self):
        super().setUp()
        self.setup_match(True, SupplyAvailabilityOption.OTG)
        self.setup_qna(answering=True, answered=True)

    def test_stray_input(self):
        self._test_stray_input(
            intents.QNA,
            messages.QNA__THANK_YOU,
            target_body_variation_key='NOT_INITIAL_BUYING'
        )

class QNAPleasePay_AnsweredNoFollowUpQuestion_Selling_Test(QNAPleasePayTest):
    """User is selling, answered seller's question, not followed up with a
    question to the seller."""
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        self.setup_qna(answering=True, answered=True)

    def test_stray_input(self):
        self._test_stray_input(
            intents.QNA,
            messages.QNA__THANK_YOU,
            target_body_variation_key='NOT_INITIAL_SELLING'
        )

class QNAPleasePay_NotAnsweredNoFollowUpQuestion_Buying_Test(QNAPleasePayTest):
    """User is buying, NOT answered seller's question, not followed up with a
    question to the seller."""

    def setUp(self):
        super().setUp()
        self.setup_match(True, SupplyAvailabilityOption.OTG)
        self.setup_qna(answering=True, answered=False)

    def test_stray_input(self):
        self._test_stray_input(
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='BUYING'
        )

class QNAPleasePay_NotAnsweredNoFollowUpQuestion_Selling_Test(QNAPleasePayTest):
    """User is selling, NOT answered seller's question, not followed up with a
    question to the seller."""
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        self.setup_qna(answering=True, answered=False)

    def test_stray_input(self):
        self._test_stray_input(
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='SELLING'
        )

class QNAPleasePay_MatchClosed_Test(QNAPleasePayTest):
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