from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewDemandDemandGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        # Set up a product, and have the user enter a term that matches the
        # known product
        _, _, kw = self.set_up_product_type(
            uom_description='200 jams in 1 jar',
            uom_plural_name='jars'
        )
        self.set_up_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        # Have the user enter a term that does not match any known product
        self.set_up_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'yWisrFJcMovxRwFyrHHH' # Unlikely term to match any known product
        )

class NewDemandGetCountryState_KnownProduct_Test(
    NewDemandDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )

class NewDemandGetCountryState_UnknownProduct_Test(
    NewDemandDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )