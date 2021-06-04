from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewDemandGetProductTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(input, intents.NEW_DEMAND, messages.DEMAND__GET_COUNTRY_STATE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            input
        )