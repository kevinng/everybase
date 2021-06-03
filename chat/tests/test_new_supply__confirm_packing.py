from chat.tests import utils
from chat.libraries import intents, messages, context_utils

class NewSupplyConfirmPackingReadyOTGKnownPackingTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

        # TODO: set up ready/otg

        # TODO: set up known packing

    def test_choose_yes_with_number(self):
        # self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)
        pass

    def test_choose_yes_with_text(self):
        pass

    def test_choose_no_with_number(self):
        pass

    def test_choose_no_with_text(self):
        pass

class NewSupplyConfirmPackingReadyOTGUnknownPackingTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

    def test_choose_yes_with_number(self):
        # self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)
        pass

    def test_choose_yes_with_text(self):
        pass

    def test_choose_no_with_number(self):
        pass

    def test_choose_no_with_text(self):
        pass

class NewSupplyConfirmPackingPreOrderTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp()
        context_utils.start_context(self.user, intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)

    def test_choose_yes_with_number(self):
        # self.receive_reply_assert('1', intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)
        pass

    def test_choose_yes_with_text(self):
        pass

    def test_choose_no_with_number(self):
        pass

    def test_choose_no_with_text(self):
        pass