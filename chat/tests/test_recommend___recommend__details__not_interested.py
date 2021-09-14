from relationships.models import Lead, Recommendation
from chat.libraries.constants import intents, messages
from chat.libraries.classes.chat_test import ChatTest

class RecommendDetailsTest():
    def _setUp(self):
        lead = Lead.objects.create(
            display_text='Example lead details',
            owner=self.user_2, # User 2 is buying
            is_buying=True
        )
        self.user.current_recommendation = Recommendation.objects.create(
            recommendee=self.user,
            lead=lead
        )

    def _test_enter_reason(self, variation_key):
        reason = 'I dun like it'
        self.receive_reply_assert(
            reason,
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRMED,
            target_body_variation_key=variation_key
        )
        r = self.user.current_recommendation
        self.assertEqual(r.recommend_details_not_interested_text, reason)

    def test_cancel(self):
        self.receive_reply_assert(
            'cancel',
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            target_body_variation_key='SELL' # User 1 is selling
        )

class RECOMMEND___RECOMMEND__DETAILS__NOT_INTERESTED___Registered___Test(
    RecommendDetailsTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            registered=True
        )
        self._setUp()

    def test_enter_reason(self):
        self._test_enter_reason('REGISTERED')

class RECOMMEND___RECOMMEND__DETAILS_NOT_INTERESTED___Unregistered___Test(
    RecommendDetailsTest, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED,
            registered=False
        )
        self._setUp()

    def test_enter_reason(self):
        self._test_enter_reason('UNREGISTERED')