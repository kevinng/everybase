from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWBuyerGetQuantityReadyOTGUnknownPackingTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
        )
        # User entered a product type string that does not match any product
        # in our product
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            '19mlI0c6pbWqOCu1eCrr' # String unlikely to match any product
        )
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING
        )
        self.assert_value(
            datas.QUANTITY,
            value_string=input
        )