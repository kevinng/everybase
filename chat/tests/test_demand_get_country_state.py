from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewDemandGetCountryStateTest(MessageHandlerTest):
    def set_up_known_product(self):
        _, _, kw = self.set_up_product_type()
        self.set_up_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def set_up_unknown_product(self):
        self.set_up_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

class NewDemandGetCountryState_KnownProduct_TestCase(
    NewDemandGetCountryStateTest):
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

class NewDemandGetCountryState_UnknownProduct_TestCase(
    NewDemandGetCountryStateTest):
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