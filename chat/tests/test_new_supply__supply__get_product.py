from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )