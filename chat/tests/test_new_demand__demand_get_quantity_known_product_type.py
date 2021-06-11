from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewDemandGetQuantityKnownProductTestCase(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )

    def test_enter_bad_value(self):
        self.receive_reply_assert(
            'hello',
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )

    def enter_quantity(self, input, target):
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.\
        NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
            value_float=target
        )

    def test_enter_quantity_1(self):
        self.enter_quantity('40', 40)

    def test_enter_quantity_2(self):
        self.enter_quantity('10.5', 10.5)