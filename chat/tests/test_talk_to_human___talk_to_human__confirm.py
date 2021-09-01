from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuTest

class TalkToHuman_TalkToHuman__Confirm_Test(ChatTest, MenuTest):
    def setUp(self):
        # Unregistered - so register option available
        super().setUp(
            intents.TALK_TO_HUMAN,
            messages.TALK_TO_HUMAN__CONFIRM
        )