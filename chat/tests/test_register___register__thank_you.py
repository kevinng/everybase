from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuRegisteredTest, MenuUnregisteredTest

class REGISTER___REGISTER__THANK_YOU___Unregistered___Test(
    MenuUnregisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU,
            registered=False
        )

class REGISTER___REGISTER__THANK_YOU___Registered_Test(
    MenuRegisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU,
            registered=True
        )