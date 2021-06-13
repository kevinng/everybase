from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewDemandDemandGetPriceKnownProductTypeTest(MessageHandlerTest):
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
            messages.DEMAND__THANK_YOU,
            texts.NEW_DEMAND__DEMAND__THANK_YOU
        )
        self.assert_value(
            datas.\
                NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING,
            value_string=input
        )