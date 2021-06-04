from chat.tests import utils
from chat.libraries import intents, messages

class SupplyThankYouTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
    
    def test_get_quantity(self):
        self.receive_reply_assert('hello', intents.MENU, messages.MENU)