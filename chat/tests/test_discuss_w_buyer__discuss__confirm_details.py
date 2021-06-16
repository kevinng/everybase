from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class DiscussWBuyerDiscussConfirmDetailsTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_DETAILS
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_DETAILS,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )
        self.assert_value(
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            value_string=datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__YES
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.assert_value(
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__CHOICE,
            value_string=datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')