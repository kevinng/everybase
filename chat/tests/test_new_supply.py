from chat import models
from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils, model_utils

class ChooseNewSupplyTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.MENU, messages.MENU)

    def test_choose_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_choose_with_text(self):
        self.receive_reply_assert('buyer', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

class GetProductTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
        self.assert_latest_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            value_string=input
        )

class GetAvailabilityTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
    
    def test_choose_ready_otg_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)

    def test_choose_ready_otg_with_text_1(self):
        self.receive_reply_assert('ready', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)

    def test_choose_ready_otg_with_text_2(self):
        self.receive_reply_assert('otg', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)


    # def test_choose_ready_otg_with_number(self):
    #     self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)

    # def test_choose_ready_otg_with_text_1(self):
    #     self.receive_reply_assert('ready', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)

    # def test_choose_ready_otg_with_text_2(self):
    #     self.receive_reply_assert('otg', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE)