from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerGetQuantityUnknownProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
        )

    def test_enter_quantity(self):
        input = '200 MT'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.\
DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING,
            value_string=input
        )