from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewDemandGetQuantityUnknownProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
        )

    def test_enter_quantity(self):
        input = '200 MT'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.QUANTITY,
            value_string=input
        )