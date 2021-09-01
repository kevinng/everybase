from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class DiscussWBuyerSupplyGetAcceptLCTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__GET_ACCEPT_LC)
        self.setup_match(False, SupplyAvailabilityOption.OTG)
    
    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_ACCEPT_LC,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            target_body_variation_key='SELLING' # We only need test as seller
        )
        self.assert_value(
            datas.ACCEPT_LC,
            value_string=datas.ACCEPT_LC__YES
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            target_body_variation_key='SELLING' # We only need test as seller
        )
        self.assert_value(
            datas.ACCEPT_LC,
            value_string=datas.ACCEPT_LC__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')