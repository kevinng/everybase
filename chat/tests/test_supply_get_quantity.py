from chat.tests import utils
from chat.libraries import intents, messages, context_utils

class NewSupplyGetQuantity_ReadyOTG_KnownPacking_Test(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING)
    
    def test_get_quantity(self):
        pass
    
