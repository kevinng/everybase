from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerDiscussAskTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ASK
        )
    
    def test_get_question(self):
        input = 'Can you do OEM?'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__THANK_YOU
        )
        self.assert_value(
            datas.QUESTION,
            value_string=input
        )