from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class DiscussWSellerDemandGetProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_SELLER, messages.DEMAND__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE,
            texts.DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE
        )
        self.assert_value(
            datas.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )