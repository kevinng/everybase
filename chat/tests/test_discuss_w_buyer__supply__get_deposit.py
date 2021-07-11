from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWBuyerSupplyGetDepositTestCase(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__GET_DEPOSIT)

    def test_enter_bad_value(self):
        self.receive_reply_assert(
            'hello',
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_DEPOSIT,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_NUMBER
        )

    def enter_deposit(self, input, target):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_ACCEPT_LC
        )
        self.assert_value(
            datas.DEPOSIT,
            value_float=target
        )

    def test_enter_deposit_1(self):
        self.enter_deposit('40', 40)

    def test_enter_deposit_2(self):
        self.enter_deposit('10.5', 10.5)