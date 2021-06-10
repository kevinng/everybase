from chat.libraries import intents, messages, datas, chat_flow_test

class NewDemandGetPrice_KnownProductType_Test(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
    
    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )
        self.assert_value(
            datas.\
                NEW_DEMAND__DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE__PRICE__STRING,
            value_string=input
        )

class NewDemandGetPrice_UnknownProductType_Test(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE
        )
    
    def test_get_price(self):
        input = 'USD 20 per box'
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__THANK_YOU
        )
        self.assert_value(
            datas.\
            NEW_DEMAND__DEMAND__GET_PRICE_UNKNOWN_PRODUCT_TYPE__PRICE__STRING,
            value_string=input
        )