from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class FIND_BUYERS___REGISTER__NAME___Test(ChatTest):
    def setUp(self):
        super().setUp(intents.FIND_BUYERS, messages.REGISTER__NAME, name=None)

    def test_enter_name(self):        
        self.receive_reply_assert(
            'Kevin Ng',
            intents.FIND_BUYERS,
            messages.REGISTER__EMAIL
        )
        self.assertEqual(self.user.name, 'Kevin Ng')