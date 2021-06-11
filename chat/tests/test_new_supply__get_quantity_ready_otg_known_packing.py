from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetQuantityReadyOTGKnownPackingTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
        self.assert_value(
            datas.\
    NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING,
            value_string=input
        )