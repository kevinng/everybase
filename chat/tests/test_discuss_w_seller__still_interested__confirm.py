from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, SupplyAvailabilityOption

class DiscussWSellerStillInterestedConfirmTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM
        )
        self.setup_buyer(SupplyAvailabilityOption.OTG)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM,
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
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU
        )
        self.assert_value(
            datas.STILL_INTERESTED,
            value_string=datas.STILL_INTERESTED__YES
        )
        self.assertNotEqual(
            self.user.current_match.buyer_still_interested,
            None
        )
        self.assertNotEqual(
            self.user.current_match.buyer_still_interested_value,
            None
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU
        )
        self.assert_value(
            datas.STILL_INTERESTED,
            value_string=datas.STILL_INTERESTED__NO
        )
        self.assertNotEqual(
            self.user.current_match.buyer_still_interested,
            None
        )
        self.assertNotEqual(
            self.user.current_match.buyer_still_interested_value,
            None
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')