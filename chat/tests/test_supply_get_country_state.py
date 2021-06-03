from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class GetCountryStateTest():
    def set_up_known_product(self):
        self.set_up_user_entered_found_product(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

    def set_up_unknown_product(self):
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

class GetCountryStateReadyOTG_KnownProduct_Test(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )

class GetCountryStateReadyOTG_UnknownProduct_Test(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG,
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )

class GetCountryStatePreOrder_KnownProduct_Test(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.set_up_known_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )

class GetCountryStatePreOrder_UnknownProduct_Test(utils.ChatFlowTest, GetCountryStateTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.set_up_unknown_product()

    def test_enter_country_state(self):
        input = 'singapore'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER,
            datas.NEW_SUPPLY__SUPPLY__GET_COUNTRY_STATE__COUNTRY_STATE__STRING,
            value_string=input
        )