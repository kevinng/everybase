from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWBuyerSupplyGetQuantityPreOrderTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
    
    def test_get_quantity(self):
        input = '10000 boxes a month'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_PRE_ORDER
        )
        self.assert_value(
            datas.QUANTITY,
            value_string=input
        )