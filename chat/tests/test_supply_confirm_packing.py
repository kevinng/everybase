from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils

class NewSupplyConfirmPacking_ReadyOTG_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_yes_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING)

    def test_choose_yes_with_text(self):
        self.receive_reply_assert('yes', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING)

    def test_choose_no_with_number(self):
        self.receive_reply_assert('2', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)

    def test_choose_no_with_text(self):
        self.receive_reply_assert('no', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)

class NewSupplyConfirmPacking_PreOrder_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_choose_yes_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_PRE_ORDER)

    def test_choose_yes_with_text(self):
        self.receive_reply_assert('yes', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_PRE_ORDER)

    def test_choose_no_with_number(self):
        self.receive_reply_assert('2', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)

    def test_choose_no_with_text(self):
        self.receive_reply_assert('no', intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)