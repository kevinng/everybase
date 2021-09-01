from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class NewDemandDemandGetCountryStateTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_COUNTRY_STATE
        )

    def setup_known_product(self):
        # Set up a product, and have the user enter a term that matches the
        # known product
        _, _, kw = self.setup_product_type(
            uom_description='200 jams in 1 jar',
            uom_plural_name='jars'
        )
        self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )

    def setup_unknown_product(self):
        # Have the user enter a term that does not match any known product
        self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.PRODUCT,
            'yWisrFJcMovxRwFyrHHH' # Unlikely term to match any known product
        )

class NewDemandGetCountryState_KnownProduct_Test(
    NewDemandDemandGetCountryStateTest):
    def setUp(self):
        super().setUp()
        self.setup_known_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )

class NewDemandGetCountryState_UnknownProduct_Test(
    NewDemandDemandGetCountryStateTest):
    def setUp(self):
        super().setUp()
        self.setup_unknown_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.COUNTRY_STATE,
            value_string=input
        )