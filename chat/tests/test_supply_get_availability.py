from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class NewSupplyGetAvailabilityTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('3', intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)

    def test_choose_non_choice_with_text(self):
        self.receive_reply_assert('hello', intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)
    
    def test_choose_ready_otg_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_ready_otg_with_text_1(self):
        self.receive_reply_assert('ready', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_ready_otg_with_text_2(self):
        self.receive_reply_assert('otg', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_preorder_with_number(self):
        self.receive_reply_assert('2', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_choose_preorder_with_text(self):
        self.receive_reply_assert('pre order', intents.NEW_SUPPLY, messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )