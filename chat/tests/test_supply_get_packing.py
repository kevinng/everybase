from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewSupplyGetPacking_ReadyOTG_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING,
            value_string=input
        )

class NewSupplyGetPacking_PreOrder_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING,
            value_string=input
        )