from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerDemandGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have the user enter a term that matches the
        # known product
        _, _, kw = self.set_up_product_type(
            uom_description='200 jams in 1 jar',
            uom_plural_name='jars'
        )
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRODUCT,
            datas.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Have the user enter a term that does not match any known product
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRODUCT,
            datas.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'yWisrFJcMovxRwFyrHHH' # Unlikely term to match any known product
        )

class DiscussWSellerGetCountryState_KnownProduct_Test(
    DiscussWSellerDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
    datas.DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )

class DiscussWSellerGetCountryState_UnknownProduct_Test(
    DiscussWSellerDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
        )
        self.assert_value(
    datas.DISCUSS_W_SELLER__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )