from chat.tests import texts
from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetQuantityReadyOTGKnownPackingTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )
        # Set up a product, and have user enter a search phrase that matches
        # this product exactly
        _, _, kw = self.set_up_product_type(uom_name='Carton')
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING,
            texts.NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
        self.assert_value(
            datas.\
    NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING,
            value_string=input
        )