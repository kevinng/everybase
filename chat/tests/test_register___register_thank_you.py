from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuTest

class Register__Register_ThankYou_Test(ChatTest, MenuTest):
    def setUp(self):
        # Unregistered - so register option available
        super().setUp(
            intents.REGISTER,
            messages.REGISTER__THANK_YOU
        )