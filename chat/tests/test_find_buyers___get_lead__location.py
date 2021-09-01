from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class FIND_BUYERS___GET_LEAD__LOCATION___Test(ChatTest):
    def setUp(self):
        super().setUp(intents.FIND_BUYERS, messages.GET_LEAD__LOCATION)

    def test_enter_bad_email(self):
        location = 'Singapore'
        self.receive_reply_assert(
            location,
            intents.FIND_BUYERS,
            messages.GET_LEAD__DETAILS
        )
        self.assert_value(
            datas.LOCATION,
            value_string=location
        )