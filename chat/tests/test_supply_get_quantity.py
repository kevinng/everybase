from chat.tests import utils
from chat.libraries import intents, messages, datas

class NewSupplyGetQuantity_ReadyOTG_KnownPacking_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING)
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING__QUANTITY__STRING,
            input
        )
    
class NewSupplyGetQuantity_ReadyOTG_UnknownPacking_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING)
    
    def test_get_quantity(self):
        input = '10000 boxes'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRICE_READY_OTG_UNKNOWN_PACKING)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING__QUANTITY__STRING,
            input
        )

class NewSupplyGetQuantity_PreOrder_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_PRE_ORDER)
    
    def test_get_quantity(self):
        input = '10000 boxes a month'
        self.receive_reply_assert(input, intents.NEW_SUPPLY, messages.SUPPLY__GET_PRICE_PRE_ORDER)
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_QUANTITY_PREORDER__QUANTITY__STRING,
            input
        )