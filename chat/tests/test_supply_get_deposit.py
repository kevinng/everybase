from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewSupplyGetDepositTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_DEPOSIT)

    def test_enter_bad_value(self):
        self.receive_reply_assert('hello', intents.NEW_SUPPLY, messages.SUPPLY__GET_DEPOSIT)

    def test_enter_deposit_1(self):
        self.receive_reply_assert('40', intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER,
            value_float=40
        )

    def test_enter_deposit_2(self):
        self.receive_reply_assert('10.5', intents.NEW_SUPPLY, messages.SUPPLY__GET_ACCEPT_LC)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER,
            value_float=10.5
        )