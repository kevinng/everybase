from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWSellerDiscussAskTest(ChatTest):
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