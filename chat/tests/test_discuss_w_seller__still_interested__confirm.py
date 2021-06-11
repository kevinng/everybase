from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class DiscussWSellerStillInterestedConfirmTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM,
            texts.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU,
            texts.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU
        )
        self.assert_value(
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE,
            value_string=datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__YES
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU,
            texts.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU
        )
        self.assert_value(
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__CHOICE,
            value_string=datas.DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')