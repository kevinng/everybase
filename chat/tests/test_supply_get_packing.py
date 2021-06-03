from chat.tests import utils
from chat.libraries import intents, messages, datas, context_utils, model_utils

class NewSupplyGetPacking_ReadyOTG_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_receive_packing(self):
        self.receive_reply_assert('100 pieces in 1 box', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING)

class NewSupplyGetPacking_PreOrder_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.set_up_data_value_string(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_receive_packing(self):
        self.receive_reply_assert('100 pieces in 1 box', intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_PRE_ORDER)