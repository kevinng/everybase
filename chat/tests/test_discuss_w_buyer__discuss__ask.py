from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class DiscussWBuyerDiscussAskTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK
        )
    
    def test_get_question(self):
        input = 'Can you do OEM?'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__THANK_YOU,
            texts.DISCUSS_W_BUYER__DISCUSS__THANK_YOU
        )
        self.assert_value(
            datas.DISCUSS_W_BUYER__DISCUSS__ASK__QUESTION__STRING,
            value_string=input
        )