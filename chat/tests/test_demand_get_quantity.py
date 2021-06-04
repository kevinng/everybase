from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewDemandGetQuantity_KnownProduct_TestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE)

    def test_enter_bad_value(self):
        self.receive_reply_assert('hello', intents.NEW_DEMAND, messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE)

    def test_enter_quantity_1(self):
        self.receive_reply_assert('40', intents.NEW_DEMAND, messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
            value_float=40
        )

    def test_enter_quantity_2(self):
        self.receive_reply_assert('10.5', intents.NEW_DEMAND, messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
            value_float=10.5
        )

class NewDemandGetQuantity_UnknownProduct_TestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE)

    def test_enter_quantity(self):
        input = '200 MT'
        self.receive_reply_assert(input, intents.NEW_DEMAND, messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE__QUANTITY__STRING,
            value_float=input
        )