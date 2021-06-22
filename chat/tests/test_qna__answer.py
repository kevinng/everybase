from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class QNAAnswerTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.ANSWER
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER_THANK_YOU
        )
        self.assert_value(
            datas.QNA__ANSWER__INPUT__STRING,
            value_string=input
        )