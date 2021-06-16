from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have the user enter a search string that will
        # match the product exactly
        _, _, kw = self.set_up_product_type(
            uom_description='200 pieces in 1 box')
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Have the user enter a string that's unlikely to match a product in
        # the database
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'nnh8aT4THy1cm84mfD5w' # Unlikely string to match a product type
        )

class NewSupplySupplyGetCountryStateReadyOTG_KnownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG
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
datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING,
            value_string=input
        )

class NewSupplySupplyGetCountryStateReadyOTG_UnknownProduct_Test(
    NewSupplySupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG
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
datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING,
            value_string=input
        )