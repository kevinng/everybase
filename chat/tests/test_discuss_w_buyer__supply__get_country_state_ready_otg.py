from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWBuyerSupplyGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have the user enter a search string that will
        # match the product exactly
        _, _, kw = self.setup_product_type(
            uom_description='200 pieces in 1 box')
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Have the user enter a string that's unlikely to match a product in
        # the database
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'nnh8aT4THy1cm84mfD5w' # Unlikely string to match a product type
        )

class DiscussWBuyerSupplyGetCountryStateReadyOTG_KnownProduct_Test(
    DiscussWBuyerSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG
        )
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__CONFIRM_PACKING
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )

class DiscussWBuyerSupplyGetCountryStateReadyOTG_UnknownProduct_Test(
    DiscussWBuyerSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG
        )
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )