from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, SupplyAvailabilityOption
from chat.libraries.utilities.get_payment_link import get_payment_link

class QNAAnswerThankYouTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.ANSWER__THANK_YOU)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def _test_choose_answer(self, target_body_variation_key):
        self.receive_reply_assert(
            '1',
            intents.QNA,
            messages.QUESTION,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(
            datas.QNA,
            value_string=datas.QNA__ASK_QUESTION
        )

    def _test_choose_buy_contact(self, target_body_variation_key):
        def get_params():
            return { 'payment_link': get_payment_link(self.payment_hash) }

        self.receive_reply_assert(
            '2',
            intents.QNA,
            messages.PLEASE_PAY,
            target_body_variation_key=target_body_variation_key,
            target_body_params_func=get_params
        )
        self.assert_value(
            datas.QNA,
            value_string=datas.QNA__BUY_CONTACT
        )

class QNAAnswerThankYou_Buying_Test(QNAAnswerThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG)
        self.setup_qna(answered=True)
        self.setup_payment_hash()

    def test_choose_answer(self):
        self._test_choose_answer('BUYING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('BUYING')

class QNAAnswerThankYou_Selling_Test(QNAAnswerThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_seller()
        self.setup_qna(answered=True)
        self.setup_payment_hash()

    def test_choose_answer(self):
        self._test_choose_answer('SELLING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('SELLING')

class QNAAnswerThankYou_MatchClosed_Test(QNAAnswerThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG, closed=True)
        self.setup_qna(answered=True)

    def test_choose_any_option(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )

    def choose_non_choice(self, input):
        # Override
        self.receive_reply_assert(
            input,
            intents.MENU,
            messages.MENU
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )