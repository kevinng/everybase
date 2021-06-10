from chat.libraries import intents, messages
from chat.libraries import MessageHandlerTest

class RegisterTestCase(MessageHandlerTest):
    def setUp(self):
        super().setUp(name=None)

    def test_register(self):
        self.receive_reply_assert(
            'Hi' ,
            intents.REGISTER,
            messages.REGISTER__GET_NAME
        )
        self.assertEqual(self.user.name, None)
        
        self.receive_reply_assert('Kevin', intents.MENU, messages.MENU)
        self.assertEqual(self.user.name, 'Kevin')