from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class NewSupplyGetAcceptLCTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('3', intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)

    def test_choose_non_choice_with_text(self):
        self.receive_reply_assert('hello', intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)
    
    def test_choose_yes_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES
        )

    def test_choose_ready_otg_with_text_1(self):
        self.receive_reply_assert('yes', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__YES
        )

    def test_choose_ready_otg_with_text_2(self):
        self.receive_reply_assert('2', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO
        )

    def test_choose_preorder_with_number(self):
        self.receive_reply_assert('no', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_ACCEPT_LC__ACCEPT_LC__NO
        )