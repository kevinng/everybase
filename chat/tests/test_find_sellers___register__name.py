from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class FIND_SELLERS___REGISTER__NAME___Test(ChatTest):
    def setUp(self):
        super().setUp(intents.FIND_SELLERS, messages.REGISTER__NAME, name=None)

    def test_enter_name(self):        
        self.receive_reply_assert(
            'Kevin Ng',
            intents.FIND_SELLERS,
            messages.REGISTER__EMAIL
        )
        self.assertEqual(self.user.name, 'Kevin Ng')