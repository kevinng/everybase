from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWSellerDemandGetPriceKnownProductTypeTest(ChatTest):
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
            messages.DISCUSS__ASK
        )
        self.assert_value(
            datas.PRICE,
            value_string=input
        )