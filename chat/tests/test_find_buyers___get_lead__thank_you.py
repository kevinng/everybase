from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import (MenuRegisteredTestBase,
    MenuUnregisteredTestBase)

class FIND_BUYERS___GET_LEAD__THANK_YOU___Unregistered___Test(
    MenuUnregisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.FIND_BUYERS,
            messages.GET_LEAD__THANK_YOU,
            registered=False
        )

class FIND_BUYERS___GET_LEAD__THANK_YOU___Registered_Test(
    MenuRegisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.FIND_BUYERS,
            messages.GET_LEAD__THANK_YOU,
            registered=True
        )