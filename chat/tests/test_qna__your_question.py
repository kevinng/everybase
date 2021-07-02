from chat.libraries.classes.context_logic import ContextLogic
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, SupplyAvailabilityOption
from chat.libraries.utilities.get_payment_link import get_payment_link

class QNAYourQuestion(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.YOUR_QUESTION)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(datas.INVALID_CHOICE, value_string=input)

    def _test_choose_answer(self, target_body_variation_key):
        self.receive_reply_assert(
            '1',
            intents.QNA,
            messages.ANSWER,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(datas.QNA, value_string=datas.QNA__ANSWER_QUESTION)

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

    def _test_choose_stop_discussion(self, target_body_variation_key):
        self.receive_reply_assert(
            '3',
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            target_body_variation_key=target_body_variation_key
        )
        self.assert_value(datas.QNA, value_string=datas.QNA__STOP_DISCUSSION)

class QNAYourQuestion_Buying_Test(QNAYourQuestion):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG)
        self.setup_payment_hash()
        self.setup_qna()

    # Note: non-choice must be tested in the subclass because the setup is not
    # complete

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self._test_choose_answer('BUYING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('BUYING')

    def test_choose_stop_discussion(self):
        self._test_choose_stop_discussion('BUYING')

class QNAYourQuestion_Selling_Test(QNAYourQuestion):
    def setUp(self):
        super().setUp()
        self.setup_seller()
        self.setup_payment_hash()
        self.setup_qna()

    # Note: non-choice must be tested in the subclass because the setup is not
    # complete

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self._test_choose_answer('SELLING')

    def test_choose_buy_contact(self):
        self._test_choose_buy_contact('SELLING')

    def test_choose_stop_discussion(self):
        self._test_choose_stop_discussion('SELLING')

class QNAYourQuestion_MatchClosed_Test(QNAYourQuestion):
    def setUp(self):
        super().setUp()
        self.setup_seller(closed=True)
        self.setup_qna()

    def test_choose_any_option(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )