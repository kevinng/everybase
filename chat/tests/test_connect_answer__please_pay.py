import datetime, pytz
from django.utils import timezone

from chat import models
from common import models as commods
from relationships import models as relmods
from payments import models as paymods

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class ConnectAnswerPleasePay_Unquestioned_Buying_Test(MessageHandlerTest):
    """User is buying and has not asked the seller a question"""
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

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
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            manual_cleaned_question='Can you do OEM?',
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_ANSWER,
            target_body_variation_key='BUYING'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectAnswerPleasePay_Unquestioned_Selling_Test(MessageHandlerTest):
    """User is selling and has not asked the seller a question"""
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

        # Set user's name
        self.user.name = 'Kevin Ng'
        self.user.save()

        # Supply - sys_user stands in as seller/questioner
        supply = self.set_up_supply()

        # Buying
        demand = relmods.Demand.objects.create(user=self.sys_user)

        # Set up match ID for your-answer
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.sys_user,
            answerer=self.user,
            manual_cleaned_question='Can you do OEM?',
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.YOUR_ANSWER,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectAnswerPleasePay_Questioned_Buying_OTG_Test(MessageHandlerTest):
    """User is buying, has asked the seller a question, and the seller's supply
    is OTG"""
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

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

        # Set up match ID from your-answer
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            answered=timezone.now(), # Answered
            manual_cleaned_question='Can you do ODM?', # Old question
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

        # User has initiated another question
        ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.QUESTION
        )
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            value_string='Can you do OEM?' # New question
        )
        relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            asked=timezone.now(), # Asked
            match=match,
            question_captured_value=dv
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QUESTION__THANK_YOU,
            target_body_variation_key='BUYING__OTG'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectAnswerPleasePay_Questioned_Buying_PreOrderDeadline_Test(MessageHandlerTest):
    """User is buying, has asked the seller a question, and the seller's supply
    has a pre-order deadline"""
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

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
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            answered=timezone.now(), # Answered
            manual_cleaned_question='Can you do ODM?', # Old question
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

        # User has initiated another question
        ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.QUESTION
        )
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            value_string='Can you do OEM?' # New question
        )
        relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            asked=timezone.now(), # Asked
            match=match,
            question_captured_value=dv
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QUESTION__THANK_YOU,
            target_body_variation_key='BUYING__PRE_ORDER_DEADLINE'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectAnswerPleasePay_Questioned_Buying_PreOrderDuration_Test(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

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
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            answered=timezone.now(), # Answered
            manual_cleaned_question='Can you do ODM?', # Old question
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

        # User has initiated another question
        ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.QUESTION
        )
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            value_string='Can you do OEM?' # New question
        )
        relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            asked=timezone.now(), # Asked
            match=match,
            question_captured_value=dv
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QUESTION__THANK_YOU,
            target_body_variation_key='BUYING__PRE_ORDER_DURATION'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )

class ConnectAnswerPleasePay_Questioned_Selling_Test(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.CONNECT_ANSWER, messages.PLEASE_PAY)

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
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Answered question
        qna = relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            answered=timezone.now(), # Answered
            manual_cleaned_question='Can you do ODM?', # Old question
            manual_cleaned_answer='Yes, we can.',
            match=match
        )
        self.set_up_data_value(
            intents.QNA,
            messages.YOUR_ANSWER,
            datas.QNA__YOUR_ANSWER__QNA_ID__ID,
            value_id=qna.id,
            inbound=False
        )

        # User has initiated another question
        ds = models.MessageDataset.objects.create(
            intent_key=intents.QNA,
            message_key=messages.QUESTION
        )
        dv = models.MessageDataValue.objects.create(
            dataset=ds,
            value_string='Can you do OEM?' # New question
        )
        relmods.QuestionAnswerPair.objects.create(
            questioner=self.user,
            answerer=self.sys_user,
            asked=timezone.now(), # Asked
            match=match,
            question_captured_value=dv
        )

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.QUESTION__THANK_YOU,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.CONNECT_ANSWER__PLEASE_PAY__STRAY_INPUT__STRING,
            value_string=input
        )