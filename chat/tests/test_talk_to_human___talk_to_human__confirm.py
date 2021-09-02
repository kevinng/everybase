from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import (MenuUnregisteredTestBase,
    MenuRegisteredTestBase)

class TALK_TO_HUMAN___TALK_TO_HUMAN__CONFIRM___Unregistered___Test(
    MenuUnregisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            registered=False
        )

class TALK_TO_HUMAN___TALK_TO_HUMAN__CONFIRM___Registered___Test(
    MenuRegisteredTestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            registered=True
        )