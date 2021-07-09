from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import (MessageHandlerTest,
    SupplyAvailabilityOption)
from chat.libraries.utility_funcs.get_payment_link import get_payment_link

class QNAThankYouTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.YOUR_ANSWER)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_ANSWER,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(datas.INVALID_CHOICE, value_string=input)

    def _test_choose_ask(self, target_body_variation_key):
        self.receive_reply_assert(
            '1',
            intents.QNA,
            messages.QUESTION,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(datas.QNA, value_string=datas.QNA__ASK_QUESTION)

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
        self.assert_value(datas.QNA, value_string=datas.QNA__BUY_CONTACT)

class QNAThankYou_Buying_Test(QNAThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(True, SupplyAvailabilityOption.OTG)
        self.setup_payment_hash()
        self.setup_qna(answered=True)

    # Note: non-choice must be tested in the subclass because the setup is not
    # complete

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self._test_choose_ask('BUYING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('BUYING')

class QNAThankYou_Selling_Test(QNAThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(False, SupplyAvailabilityOption.OTG)
        self.setup_payment_hash()
        self.setup_qna()

    # Note: non-choice must be tested in the subclass because the setup is not
    # complete

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self._test_choose_ask('SELLING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('SELLING')

class QNAThankYou_MatchClosed_Test(QNAThankYouTest):
    def setUp(self):
        super().setUp()
        self.setup_user_lead(False, SupplyAvailabilityOption.OTG, True)
        self.setup_qna(answered=True)

    def test_choose_any_option(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )