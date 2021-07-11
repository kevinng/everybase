from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class NewDemandDemandGetPriceKnownProductTypeTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
    
    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )
        self.assert_value(
            datas.PRICE,
            value_string=input
        )