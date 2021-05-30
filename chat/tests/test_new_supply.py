from chat import models
from chat.tests import utils
from chat.libraries import intents, messages, context_utils

class ChooseNewSupplyTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.MENU, messages.MENU)

    def test_choose_with_number(self):
        self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_choose_with_text(self):
        self.receive_reply_assert('buyer', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)