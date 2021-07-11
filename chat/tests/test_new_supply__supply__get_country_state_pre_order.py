from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class NewSupplySupplyGetCountryStateTest(ChatTest):
    def setup_known_product(self):
        # Set up a product, and have user enter a search phrase that matches
        # this product exactly
        _, _, kw = self.setup_product_type(
            uom_description='200 pieces in 1 box')
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )

    def setup_unknown_product(self):
        # Set up the user to enter a string that's unlikely to match a known
        # product
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'SR2EdiLuc1K1BUAVsPg4' # Unlikely string to match a known product
        )

class NewSupplySupplyGetCountryStatePreOrder_KnownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        )
        self.setup_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__CONFIRM_PACKING
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )

class NewSupplySupplyGetCountryStatePreOrder_UnknownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        )
        self.setup_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )