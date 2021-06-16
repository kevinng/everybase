from chat.libraries import intents, messages
from chat.libraries.message_handler_test import MessageHandlerTest

class DiscussWSellerDiscussAlreadyConnectedTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            name='Kevin Ng'
        )

    def test_any_input(self):
        self.receive_reply_assert(
            'hello',
            intents.MENU,
            messages.MENU
        )