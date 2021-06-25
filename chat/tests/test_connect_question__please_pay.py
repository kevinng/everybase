from django.utils import timezone
import datetime, pytz

from relationships import models as relmods
from common import models as commods
from payments import models as paymods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class ConnectQuestionPleasePay_Unanswered_Buying_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Set user's name
        self.user.name = 'Kevin Ng'
        self.user.save()

        # Supply - sys_user stands in as seller/questioner
        supply = relmods.Supply.objects.create(user=self.sys_user)

        # Buying
        demand = self.set_up_demand()

        # Set up match ID from your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Unanswered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='BUYING'
        )
        self.assert_value(
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectQuestionPleasePay_Unanswered_Selling_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Set user's name
        self.user.name = 'Kevin Ng'
        self.user.save()

        # Supply from this user
        supply = self.set_up_supply()

        # Buying - sys_user stands in as seller/questioner
        demand = relmods.Demand.objects.create(user=self.sys_user)

        # Set up match ID for your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Unanswered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectQuestionPleasePay_Answered_Buying_OTG_Test(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Supply and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        supply = relmods.Supply.objects.create(
            user=self.sys_user, # sys_user stands in for seller
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            availability=relmods.Availability.objects.get(pk=1), # OTG
            quantity=12000,
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1), # USD
            deposit_percentage=0.4,
            accept_lc=False
        )

        # Buying
        demand = self.set_up_demand()

        # Set up match ID from your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            answered=timezone.now(),
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_variation_key='BUYING__OTG'
        )
        self.assert_value(
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectQuestionPleasePay_Answered_Buying_PreOrderDeadline_Test(
    MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Supply and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        pre_order_timeframe = relmods.TimeFrame.objects.create(
            deadline=datetime.datetime(2021, 2, 5, tzinfo=pytz.UTC)
        )
        supply = relmods.Supply.objects.create(
            user=self.sys_user, # sys_user stands in for seller
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            availability=relmods.Availability.objects.get(pk=2), # Pre-order
            quantity=12000,
            pre_order_timeframe=pre_order_timeframe, # 5 Feb 2021
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1), # USD
            deposit_percentage=0.4,
            accept_lc=False
        )

        # Buying
        demand = self.set_up_demand()

        # Set up match ID from your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            answered=timezone.now(),
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_variation_key='BUYING__PRE_ORDER_DEADLINE'
        )
        self.assert_value(
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectQuestionPleasePay_Answered_Buying_PreOrderDeadline_Test(
    MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Supply and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        pre_order_timeframe = relmods.TimeFrame.objects.create(
            duration_uom='d',
            duration=5
        )
        supply = relmods.Supply.objects.create(
            user=self.sys_user, # sys_user stands in for seller
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            availability=relmods.Availability.objects.get(pk=2), # Pre-order
            quantity=12000,
            pre_order_timeframe=pre_order_timeframe, # 5 days
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1), # USD
            deposit_percentage=0.4,
            accept_lc=False
        )

        # Buying
        demand = self.set_up_demand()

        # Set up match ID from your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            answered=timezone.now(),
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU,
            target_body_variation_key='BUYING__PRE_ORDER_DURATION'
        )
        self.assert_value(
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectQuestionPleasePay_Answered_Selling_Test(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.CONNECT_QUESTION,
            messages.PLEASE_PAY
        )

        # Supply and relevant models
        supply = self.set_up_supply()

        # Demand and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        demand = relmods.Demand.objects.create(
            user=self.sys_user, # sys_user stands in for buyer
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            quantity=12000,
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1) # USD
        )

        # Set up match ID from your-question
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            answered=timezone.now(),
            manual_cleaned_question='Can you do OEM?',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_QUESTION,
            datas.QNA__YOUR_QUESTION__QNA_ID__ID,
            value_id=qna.id,
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
            datas.CONNECT_QUESTION__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )