from chat.libraries.constants import datas, intents, messages
from chat.libraries.classes.chat_test import ChatTest

class DiscussWBuyerDiscussAlreadyConnectedTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ALREADY_CONNECTED
        )

    def test_any_input(self):
        target = 'hello'
        self.receive_reply_assert(
            target,
            intents.MENU,
            messages.MENU
        )
        self.assert_value(
            datas.STRAY_INPUT,
            target
        )