from relationships.models import Lead
from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class FIND_BUYERS___GET_LEAD__DETAILS___Test(ChatTest):
    def setUp(self):
        super().setUp(intents.FIND_BUYERS, messages.GET_LEAD__DETAILS)
        self.user.current_lead = Lead.objects.create(
            owner=self.user,
            is_buying=False
        )

    def test_enter_media(self):
        self.receive_reply_assert(
            '',
            intents.FIND_BUYERS,
            messages.GET_LEAD__DETAILS,
            target_body_message_key=messages.GET_LEAD__DETAILS_PROMPT,
            content_type='image/jpeg',
            url='https://everybase.co/image.jpg'
        )
    
    def test_enter_text(self):
        self.receive_reply_assert(
            'hello world',
            intents.FIND_BUYERS,
            messages.GET_LEAD__DETAILS,
            target_body_message_key=messages.GET_LEAD__DETAILS_PROMPT
        )
    
    def test_done(self):
        self.receive_reply_assert(
            'done',
            intents.FIND_BUYERS,
            messages.GET_LEAD__THANK_YOU
        )