from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWBuyerSupplyGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have the user enter a search string that will
        # match the product exactly
        _, _, kw = self.set_up_product_type(
            uom_description='200 pieces in 1 box')
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Have the user enter a string that's unlikely to match a product in
        # the database
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.DISCUSS_W_BUYER__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
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
        self.assert_value(datas.\
    DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING,
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
        self.assert_value(datas.\
    DISCUSS_W_BUYER__SUPPLY__GET_COUNTRY_STATE_READY_OTG__COUNTRY_STATE__STRING,
            value_string=input
        )