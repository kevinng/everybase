from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class GetProductTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )