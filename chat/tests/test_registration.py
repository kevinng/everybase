from chat.constants import intents, messages
from chat.tests.library import ChatTest
from chat.tasks.send_register_confirm import (send_register_confirm,
    _USER_DOES_NOT_EXIST, _CHATBOT_USER_DOES_NOT_EXIST)
from chat.utilities.render_message import render_message

class RegisterTest(ChatTest):
    def setUp(self):
        super().setUp(intents.REGISTER, messages.REGISTER__CONFIRM)

    def test_enter_yes(self):
        self.receive_reply_assert(
            'yes',
            intents.REGISTER,
            messages.REGISTER__CONFIRMED
        )

    def test_enter_unrecognized_input(self):
        self.receive_reply_assert(
            'huh',
            intents.REGISTER,
            messages.REGISTER__CONFIRM,
            target_body_message_key=messages.REGISTER__DO_NOT_UNDERSTAND
        )

class SendRegisterConfirmTest(ChatTest):
    fixtures = [
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20211126__relationships__user'
    ]

    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send_register_confirm(self):
        msg = send_register_confirm(self.user.id, True)
        self.assert_context_body(
            intents.REGISTER,
            messages.REGISTER__CONFIRM,
            msg.body, {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        )