from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class RegisterRegisterGetNameTest(ChatTest):
    def setUp(self):
        super().setUp(name=None)

    def test_register(self):
        self.receive_reply_assert(
            'Hi' ,
            intents.REGISTER,
            messages.REGISTER__GET_NAME
        )
        self.assertEqual(self.user.name, None)
        
        self.receive_reply_assert(
            'Kevin Ng',
            intents.MENU,
            messages.MENU
        )
        self.assertEqual(self.user.name, 'Kevin Ng')