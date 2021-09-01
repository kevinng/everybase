from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuUnregisteredTest, MenuRegisteredTest

class TalkToHuman_TalkToHuman__Confirm_Unregistered_Test(
    MenuUnregisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            registered=False
        )

class TalkToHuman_TalkToHuman__Confirm_Registered_Test(
    MenuRegisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM,
            registered=True
        )