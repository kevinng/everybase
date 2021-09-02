from relationships.models import Lead, Recommendation
from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class RECOMMEND___RECOMMEND__DETAILS__NOT_INTERESTED___Registered___Test(
    ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            registered=True
        )
        lead = Lead.objects.create(owner=self.user_2)
        self.user.current_recommendation = Recommendation.objects.create(
            recommendee=self.user,
            lead=lead
        )

    def test_enter_reason(self):
        reason = 'I dun like it'
        self.receive_reply_assert(
            reason,
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRM,
            target_body_variation_key='REGISTERED'
        )
        r = self.user.current_recommendation
        self.assertEqual(r.not_interested_details_reason, reason)

class RECOMMEND___RECOMMEND__DETAILS_NOT_INTERESTED___Unregistered___Test(
    ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            registered=False
        )
        lead = Lead.objects.create(owner=self.user_2)
        self.user.current_recommendation = Recommendation.objects.create(
            recommendee=self.user,
            lead=lead
        )

    def test_enter_reason(self):
        reason = 'I dun like it'
        self.receive_reply_assert(
            reason,
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRM,
            target_body_variation_key='UNREGISTERED'
        )
        r = self.user.current_recommendation
        self.assertEqual(r.not_interested_details_reason, reason)