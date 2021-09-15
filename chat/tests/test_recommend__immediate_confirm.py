from django.db import transaction
from relationships.models import Lead, ProductType, Recommendation
from chat.libraries.constants import datas, intents, messages
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.utility_funcs.render_message import render_message
from chat.tasks.send_recommend_product_type import send_recommend_product_type

class Test(ChatTest):
    fixtures = [
        'setup/20210527__relationships__producttype.json',
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20210527__relationships__user'
    ]

    def setUp(self):
        super().setUp(
            intent_key=intents.RECOMMEND,
            message_key=messages.RECOMMEND__IMMEDIATE_CONFIRM,
            registered=True
        )

        # Set up models
        p = ProductType.objects.get(pk=1) # Nitrile Gloves
        l = Lead.objects.create(
            owner=self.user_2,
            product_type=p,
            display_text='Example lead details',
            is_buying=True # User 2 is buying
        )
        self.user.current_recommendation = Recommendation.objects.create(
            lead=l,
            recommendee=self.user
        )

    def test_yes(self):
        self.receive_reply_assert(
            '1',
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            target_body_variation_key='REGISTERED'
        )
        self.assertIsNotNone(
        self.user.current_recommendation.recommend_immediate_confirm_responded)
        self.assertEqual(
            self.user.current_recommendation.recommend_immediate_confirm_choice,
            datas.RECOMMEND__IMMEDIATE_CONFIRM__YES
        )
    
    def test_cancel(self):
        self.receive_reply_assert(
            '2',
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            target_body_variation_key='SELL' # User 1 is selling
        )
        self.assertIsNotNone(
        self.user.current_recommendation.recommend_immediate_confirm_responded)
        self.assertEqual(
            self.user.current_recommendation.recommend_immediate_confirm_choice,
            datas.RECOMMEND__IMMEDIATE_CONFIRM__CANCEL
        )