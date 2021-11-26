from chat.constants import intents, messages
from chat.tests.library import ChatTest

class RegisterConfirmTest(ChatTest):
    def setUp(self):
        super().setUp(intents.REGISTER, messages.REGISTER__CONFIRM)

    def test_enter_yes(self):
        self.receive_reply_assert(
            'yes',
            intents.REGISTER,
            messages.REGISTER__CONFIRMED
        )

    # def test_enter_unrecognized_input(self):
    #     pass