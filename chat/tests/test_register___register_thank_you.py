from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuRegisteredTest, MenuUnregisteredTest

class Register__Register_ThankYou_Unregistered_Test(
    MenuUnregisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU,
            registered=False
        )

class Register__Register_ThankYou_Registered_Test(
    MenuRegisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU,
            registered=True
        )