from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class DiscussWBuyerSupplyGetQuantityPreOrderTest(MessageHandlerTest):
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
        datas.DISCUSS_W_BUYER__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING,
            value_string=input
        )