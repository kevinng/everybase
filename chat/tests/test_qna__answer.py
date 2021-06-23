from relationships import models as relmods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class QNAAnswer_Buying_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.ANSWER
        )

        # Set up supply - from seller. We use system user to stand-in for the
        # seller.
        supply = relmods.Supply.objects.create(user=self.sys_user)

        # Set up demand - from this user.
        demand = self.set_up_demand()

        # Set up match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        # Set up match ID
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_variation_key='BUYING'
        )
        self.assert_value(
            datas.QNA__ANSWER__INPUT__STRING,
            value_string=input
        )

class QNAAnswer_Selling_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.ANSWER
        )

        # Set up supply - from this user.        
        supply = self.set_up_supply()

        # Set up demand - from buyer. We use system user to stand-in for the
        # buyer.
        demand = relmods.Demand.objects.create(user=self.sys_user)

        # Set up match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        # Set up match ID
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.QNA__ANSWER__INPUT__STRING,
            value_string=input
        )