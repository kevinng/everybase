# from django.db import transaction
from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class FIND_BUYERS___GET_LEAD__LOCATION___Test(ChatTest):
    def setUp(self):
        super().setUp(intents.FIND_BUYERS, messages.GET_LEAD__DETAILS)
        
    def test_

    # def test_enter_location(self):
    #     location = 'Singapore'
    #     with transaction.atomic():
    #         self.receive_reply_assert(
    #             location,
    #             intents.FIND_BUYERS,
    #             messages.GET_LEAD__DETAILS
    #         )
    #     self.assertEqual(self.user.current_lead.location, location)