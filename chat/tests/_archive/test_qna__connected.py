from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class QNAConnectedTest(ChatTest):
    def setUp(self):
        super().setUp(intents.QNA, messages.CONNECTED)

    def test_stray_input(self):
        self.receive_reply_assert(
            'Hello world',
            intents.MENU,
            messages.MENU
        )