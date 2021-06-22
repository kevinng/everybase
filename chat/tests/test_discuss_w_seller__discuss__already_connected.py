from chat.libraries.constants import datas, intents, messages
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerDiscussAlreadyConnectedTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            name='Kevin Ng'
        )

    def test_any_input(self):
        target = 'hello'
        self.receive_reply_assert(
            target,
            intents.MENU,
            messages.MENU
        )
        self.assert_value(
    datas.DISCUSS_W_SELLER__DISCUSS__ALREADY_CONNECTED__INVALID_CHOICE__STRING,
            target
        )
