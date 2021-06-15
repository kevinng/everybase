from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewSupplySupplyGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have user enter a search phrase that matches
        # this product exactly
        _, _, kw = self.set_up_product_type(
            uom_description='200 pieces in 1 box')
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Set up the user to enter a string that's unlikely to match a known
        # product
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'SR2EdiLuc1K1BUAVsPg4' # Unlikely string to match a known product
        )

class NewSupplySupplyGetCountryStatePreOrder_KnownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        )
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__CONFIRM_PACKING
        )
        self.assert_value(
datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING,
            value_string=input
        )

class NewSupplySupplyGetCountryStatePreOrder_UnknownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        )
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_PRE_ORDER__COUNTRY_STATE__STRING,
            value_string=input
        )