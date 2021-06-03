from chat.tests import utils
from chat.libraries import intents, messages

class RegisterTestCase(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(name=None)

    def test_register(self):
        self.receive_reply_assert('Hi' , intents.REGISTER, messages.REGISTER__GET_NAME)
        self.assertEqual(self.user.name, None)
        
        self.receive_reply_assert('Kevin', intents.MENU, messages.MENU)
        self.assertEqual(self.user.name, 'Kevin')