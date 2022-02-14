from chat.constants import intents, messages
from chat.tests.library import ChatTest
from chat.tasks.send_login_message import send_login_message
from relationships import models

class LoginTest(ChatTest):
    def setUp(self):
        super().setUp(intents.LOGIN, messages.LOGIN__CONFIRM)

        # User requests for a login token
        models.LoginToken.objects.create(user=self.user)

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

class LoginConfirmTest(ChatTest):
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send_login_message(self):
        msg = send_login_message(self.user.id, True)
        self.assert_context_body(
            intents.LOGIN,
            messages.LOGIN__CONFIRM,
            msg.body, {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        )