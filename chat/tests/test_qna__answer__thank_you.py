from django.utils import timezone

from relationships import models as relmods
from payments import models as paymods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest
from chat.libraries.utilities.get_payment_link import get_payment_link

class QNAAnswerThankYou_Buying_Test(MessageHandlerTest):
    fixtures = [
        'setup/20210528__payments__currency.json'
    ]

    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.ANSWER__THANK_YOU
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

        # Set up payment hash
        usd = paymods.Currency.objects.get(pk=1)
        self._hash = paymods.PaymentHash.objects.create(
            user=self.user,
            match=match,
            currency=usd,
            unit_amount=5.67
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__INVALID_CHOICE__STRING,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self.receive_reply_assert(
            '1',
            intents.QNA,
            messages.QUESTION,
            target_body_variation_key='BUYING'
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__ASK_QUESTION
        )

    def _get_please_pay_params(self):
        return {
            'payment_link': get_payment_link(self._hash.id)
        }

    def test_choose_buy_contact(self):
        self.receive_reply_assert(
            '2',
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY,
            target_body_variation_key='BUYING',
            target_body_params_func=self._get_please_pay_params
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__BUY_CONTACT
        )

    def test_choose_stop_discussion(self):
        self.receive_reply_assert(
            '3',
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            target_body_variation_key='BUYING'
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__STOP_DISCUSSION
        )

class QNAAnswerThankYou_Selling_Test(MessageHandlerTest):
    fixtures = [
        'setup/20210528__payments__currency.json'
    ]

    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.ANSWER__THANK_YOU
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

        # Set up payment hash
        usd = paymods.Currency.objects.get(pk=1)
        self._hash = paymods.PaymentHash.objects.create(
            user=self.user,
            match=match,
            currency=usd,
            unit_amount=5.67
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__INVALID_CHOICE__STRING,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def test_choose_answer(self):
        self.receive_reply_assert(
            '1',
            intents.QNA,
            messages.QUESTION,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__ASK_QUESTION
        )

    def _get_please_pay_params(self):
        return {
            'payment_link': get_payment_link(self._hash.id)
        }

    def test_choose_buy_contact(self):
        self.receive_reply_assert(
            '2',
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY,
            target_body_variation_key='SELLING',
            target_body_params_func=self._get_please_pay_params
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__BUY_CONTACT
        )

    def test_choose_stop_discussion(self):
        self.receive_reply_assert(
            '3',
            intents.QNA,
            messages.STOP_DISCUSSION__REASON,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.QNA__ANSWER__THANK_YOU__OPTION__CHOICE,
            value_string=datas.QNA__ANSWER__THANK_YOU__OPTION__STOP_DISCUSSION
        )

class QNAAnswerThankYou_MatchClosed_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.YOUR_QUESTION
        )

        # Set user's name
        self.user.name = 'Kevin Ng'
        self.user.save()
        
        # Set up supply - from seller. We use system user to stand-in for the
        # seller.
        supply = relmods.Supply.objects.create(user=self.sys_user)

        # Set up demand - from this user.
        demand = self.set_up_demand()

        # Set up match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand,
            closed=timezone.now()
        )

        # Set up match ID
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

    def test_choose_any_option(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )