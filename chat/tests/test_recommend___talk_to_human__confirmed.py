from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import (MenuUnregisteredTestBase,
    MenuRegisteredTestBase)

class RECOMMEND___TALK_TO_HUMAN__CONFIRMED___Unregistered___Test(
    MenuUnregisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            registered=False
        )

class RECOMMEND___TALK_TO_HUMAN__CONFIRMED___Registered___Test(
    MenuRegisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            registered=True
        )