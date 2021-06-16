from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class DiscussWSellerDemandGetPriceKnownProductTypeTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
    
    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__THANK_YOU
        )
        self.assert_value(
    datas.DISCUSS_W_SELLER__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING,
            value_string=input
        )