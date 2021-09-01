from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class DiscussWBuyerDiscussConfirmDetailsTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_DETAILS
        )
        self.setup_match(False, SupplyAvailabilityOption.OTG)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_DETAILS,
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

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.CONFIRM_DETAILS,
            value_string=datas.CONFIRM_DETAILS__YES
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details,
            None
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details_correct,
            None
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details_correct_value,
            None
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.CONFIRM_DETAILS,
            value_string=datas.CONFIRM_DETAILS__NO
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details,
            None
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details_correct,
            None
        )
        self.assertNotEqual(
            self.user.current_match.seller_confirmed_details_correct_value,
            None
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')