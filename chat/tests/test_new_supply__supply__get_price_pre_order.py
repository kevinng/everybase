from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewSupplyGetPricePreOrderTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PRICE_PRE_ORDER)
    
    def test_get_quantity(self):
        input = 'USD 20 per box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_DEPOSIT
        )
        self.assert_value(
            datas.PRICE,
            value_string=input
        )