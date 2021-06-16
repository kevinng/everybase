from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetAcceptLCTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)
    
    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
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
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES
        )
    
    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')