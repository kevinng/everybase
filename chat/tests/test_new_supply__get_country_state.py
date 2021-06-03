from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils
from relationships import models as relmods
from common import models as commods
        
class GetCountryStateReadyOTG_KnownProduct_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_user_entered_found_product(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

class GetCountryStatePreOrder_KnownProduct_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_user_entered_found_product(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

class GetCountryStateReadyOTG_UnknownProduct_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)

class GetCountryStatePreOrder_UnknownProduct_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.set_up_user_entered_found_product(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING
        )
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'unknown product'
        )

    def test_enter_country_state(self):
        self.receive_reply_assert('singapore', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)