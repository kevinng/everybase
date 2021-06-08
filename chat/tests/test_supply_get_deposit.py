from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewSupplyGetDepositTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_DEPOSIT)

    def test_enter_bad_value(self):
        self.receive_reply_assert(
            'hello',
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_DEPOSIT
        )

    def enter_deposit(self, input, target):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_ACCEPT_LC
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_DEPOSIT__DEPOSIT__NUMBER,
            value_float=target
        )

    def test_enter_deposit_1(self):
        self.enter_deposit('40', 40)

    def test_enter_deposit_2(self):
        self.enter_deposit('10.5', 10.5)