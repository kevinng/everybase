from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.tests.test_menu___menu import MenuRegisteredTest, MenuUnregisteredTest

class FIND_SELLERS___GET_LEAD__THANK_YOU___Unregistered___Test(
    MenuUnregisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.FIND_SELLERS,
            messages.GET_LEAD__THANK_YOU,
            registered=False
        )

class FIND_SELLERS___GET_LEAD__THANK_YOU___Registered_Test(
    MenuRegisteredTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.FIND_SELLERS,
            messages.GET_LEAD__THANK_YOU,
            registered=True
        )