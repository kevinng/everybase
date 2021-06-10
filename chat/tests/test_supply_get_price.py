from chat.libraries import intents, messages, datas, chat_flow_test

class NewSupplyGetPrice_ReadyOTG_KnownPacking_Test(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
    
    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )
        self.assert_value(
            datas.\
        NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING__PRICE__STRING,
            value_string=input
        )
    
class NewSupplyGetPrice_ReadyOTG_UnknownPacking_Test(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING
        )
    
    def test_get_quantity(self):
        input = 'USD 20 per box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )
        self.assert_value(
            datas.\
        NEW_SUPPLY__SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING__PRICE__STRING,
            value_string=input
        )

class NewSupplyGetPrice_PreOrder_Test(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PRICE_PRE_ORDER)
    
    def test_get_quantity(self):
        input = 'USD 20 per box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_DEPOSIT
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PRICE_PREORDER__PRICE__STRING,
            value_string=input
        )