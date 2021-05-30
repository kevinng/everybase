from chat.tests import utils
from chat.libraries import intents, messages

class RegisterTestCase(utils.ChatFlowTest):
    def setUp(self):
        self.setup_user(None)

    def tearDown(self):
        self.tear_down_user()

    def test_register(self):
        # User says hi
        msg_1 = self.receive('Hi')

        # Reply
        self.reply(msg_1)

        # Test
        self.assert_context(intents.REGISTER, messages.REGISTER__GET_NAME)
        self.assertEqual(self.user.name, None)

        # User gives name
        msg_2 = self.receive('Kevin')

        # Reply
        self.reply(msg_2)

        # Test
        self.assert_context(intents.MENU, messages.MENU)
        self.assertEqual(self.user.name, 'Kevin')