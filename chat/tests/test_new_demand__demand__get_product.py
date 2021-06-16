from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewDemandDemandGetProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )