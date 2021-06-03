from chat.tests import utils
from chat.libraries import intents, messages, context_utils

class ChooseNewSupplyTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.MENU, messages.MENU, None)

    def test_choose_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_choose_with_text(self):
        self.receive_reply_assert('buyer', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)