from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWBuyerSupplyGetProductTest(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY
        )
        self.assert_value(
            datas.PRODUCT,
            value_string=input
        )