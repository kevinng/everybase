from chat.tests import utils
from chat.libraries import intents, messages

class RegisterTestCase(utils.ChatFlowTest):
    def test_register(self):
        # User says hi
        self.receive_reply('Hi')

        # Test
        self.assert_context(intents.REGISTER, messages.REGISTER__GET_NAME)
        self.assertEqual(self.user.name, None)

        # User gives name
        self.receive_reply('Kevin')

        # Test
        self.assert_context(intents.MENU, messages.MENU)
        self.assertEqual(self.user.name, 'Kevin')