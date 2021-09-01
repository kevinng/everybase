from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class register__register_email_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.REGISTER, messages.REGISTER__EMAIL, name=None)

    def test_enter_email(self):        
        self.receive_reply_assert(
            'kevin@everybase.co',
            intents.REGISTER,
            messages.REGISTER__EMAIL
        )
        self.assertEqual(self.user.email.email, 'kevin@everybase.co')

    def test_enter_bad_email(self):
        bad_email = 'hello world'
        self.receive_reply_assert(
            bad_email,
            intents.REGISTER,
            messages.REGISTER__EMAIL,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_EMAIL
        )
        self.assert_value(
            datas.STRAY_INPUT,
            value_string=bad_email
        )