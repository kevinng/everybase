from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class NewSupplyGetCountryStateTest():
    def set_up_known_product(self):
        self.set_up_user_entered_known_product_type(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

    def set_up_unknown_product(self):
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

class NewSupplyGetCountryStateReadyOTG_KnownProduct_Test(utils.ChatFlowTest, NewSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )

class NewSupplyGetCountryStateReadyOTG_UnknownProduct_Test(utils.ChatFlowTest, NewSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )

class NewSupplyGetCountryStatePreOrder_KnownProduct_Test(utils.ChatFlowTest, NewSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )

class NewSupplyGetCountryStatePreOrder_UnknownProduct_Test(utils.ChatFlowTest, NewSupplyGetCountryStateTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            input
        )