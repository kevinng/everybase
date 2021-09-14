from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import (MenuRegisteredTestBase,
    MenuUnregisteredTestBase)

class RECOMMEND___RECOMMEND__NOT_INTERESTED_CONFIRM___Unregistered___Test(
    MenuUnregisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRMED,
            registered=False
        )

class RECOMMEND___RECOMMEND__NOT_INTERESTED_CONFIRM___Registered_Test(
    MenuRegisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRMED,
            registered=True
        )