from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetQuantityReadyOTGKnownPackingTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )
        # Set up a product, and have user enter a search phrase that matches
        # this product exactly
        _, _, kw = self.setup_product_type(uom_name='Carton')
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
        self.assert_value(
            datas.QUANTITY,
            value_string=input
        )