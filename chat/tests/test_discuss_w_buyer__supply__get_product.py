from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class DiscussWBuyerSupplyGetProductTest(MessageHandlerTest):
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
            datas.DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )