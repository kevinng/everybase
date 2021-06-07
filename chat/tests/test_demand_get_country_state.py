from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewDemandGetCountryStateTest():
    def set_up_known_product(self):
        self.set_up_user_entered_known_product(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

    def set_up_unknown_product(self):
        self.set_up_data_value_string(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

class NewDemandGetCountryState_KnownProduct_TestCase(utils.ChatFlowTest,
    NewDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_COUNTRY_STATE)
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(input, intents.NEW_DEMAND, messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )

class NewDemandGetCountryState_UnknownProduct_TestCase(utils.ChatFlowTest,
    NewDemandGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_DEMAND, messages.DEMAND__GET_COUNTRY_STATE)
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'canada vancouver'
        self.receive_reply_assert(input, intents.NEW_DEMAND, messages.DEMAND__GET_QUANTITY_UNKNOWN_PRODUCT_TYPE)
        self.assert_value(
            datas.NEW_DEMAND__DEMAND__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )