from chat.constants import intents, messages
from chat.tests.library import ChatTest

class LoginTest(ChatTest):
    def setUp(self):
        super().setUp(intents.LOGIN, messages.LOGIN__CONFIRM)

    #TODO: we need to implement the task that sends out the initial message

    def test_enter_yes(self):
        self.receive_reply_assert(
            'yes',
            intents.LOGIN,
            messages.LOGIN__CONFIRMED
        )

    def test_enter_unrecognized_input(self):
        self.receive_reply_assert(
            'huh',
            intents.LOGIN,
            messages.LOGIN__CONFIRM,
            target_body_message_key=messages.LOGIN__DO_NOT_UNDERSTAND
        )