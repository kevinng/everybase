from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewSupplySupplyGetQuantityPreOrderTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
    
    def test_get_quantity(self):
        input = '10000 boxes a month'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_PRE_ORDER,
            texts.NEW_SUPPLY__SUPPLY__GET_PRICE_PRE_ORDER
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING,
            value_string=input
        )