from chat.libraries.constants import intents, messages
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class QNAConnectedTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.QNA, messages.CONNECTED)

    def test_stray_input(self):
        self.receive_reply_assert(
            'Hello world',
            intents.MENU,
            messages.MENU
        )