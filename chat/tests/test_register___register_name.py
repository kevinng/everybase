from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class register__register_name_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.REGISTER, messages.REGISTER__NAME, name=None)

    def test_enter_name(self):        
        self.receive_reply_assert(
            'Kevin Ng',
            intents.REGISTER,
            messages.REGISTER__EMAIL
        )
        self.assertEqual(self.user.name, 'Kevin Ng')