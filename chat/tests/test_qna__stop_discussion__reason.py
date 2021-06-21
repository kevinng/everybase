from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class StopDiscussionReasonTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.STOP_DISCUSSION__REASON
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.STOP_DISCUSSION__THANK_YOU
        )
        self.assert_value(
            datas.QNA__STOP_DISCUSSION__REASON__INPUT__STRING,
            value_string=input
        )