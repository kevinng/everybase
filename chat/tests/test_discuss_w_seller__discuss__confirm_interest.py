import datetime, pytz
from urllib.parse import urljoin
from django.urls import reverse
from django.utils import timezone

from everybase import settings

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest
from chat.libraries.utilities.connect import connect

from relationships import models as relmods
from common import models as commods
from payments import models as paymods

class DiscussWSellerDiscussConfirmInterestTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json',
        'setup/20210527__relationships__phonenumbertype.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            None
        )

        # User 1 ID, set by system when sending this message to the user
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID,
            value_id=self.user.id,
            inbound=False
        )

        # User 2, set by system when sending this message to the user
        self.user_2, _ = self.create_user_phone_number(
            'Test Seller', '23456', '2345678901')
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID,
            value_id=self.user_2.id,
            inbound=False
        )

    def get_target_body_params(self):
        """Helper function to render the template with the WhatsApp URL after it
        has been generated by the handler.
        """
        # There should be only 1 hash
        hash = relmods.PhoneNumberHash.objects.get(user=self.user)
        whatsapp_url = urljoin(settings.BASE_URL,
            reverse('chat_root:whatsapp', kwargs={ 'id': hash.id }))

        return { 'whatsapp_url': whatsapp_url }

class DiscussWSellerDiscussConfirmInterestTest_NotConnected_YesNo_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()

        # Demand and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        demand = self.set_up_demand(
            product_type=product_type,
            packing=packing,
            country=commods.Country.objects.get(pk=601), # Israel
            quantity=12000,
            price=15.15,
            currency=paymods.Currency.objects.get(pk=1) # USD
        )

        # Dummy supply
        supply = self.set_up_supply()

        # Match ID, set by system when sending message
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.\
            DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INVALID_CHOICE__STRING,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_DETAILS
        )
        self.assert_value(
            datas.\
                DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM
        )
        self.assert_value(
            datas.\
                DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_OTG_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Dummy demand
        demand = self.set_up_demand()

        # Supply and relevant models
        product_type, packing, _ = self.set_up_product_type(
            name='Nitrile Gloves',
            uom_name='Box',
            uom_plural_name='Boxes',
            uom_description='200 pieces in 1 box'
        )
        supply = self.set_up_supply(
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

        # Match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        # Match ID, set by system when sending message
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Connect user
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='OTG',
            target_body_params_func=self.get_target_body_params
        )
        self.assert_value(
            datas.\
                DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class \
DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_PreOrderDuration_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Dummy demand
        demand = self.set_up_demand()

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
        supply = self.set_up_supply(
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

        # Match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        # Match ID, set by system when sending message
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Connect user
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='PRE_ORDER_DURATION',
            target_body_params_func=self.get_target_body_params
        )
        self.assert_value(
            datas.\
                DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class \
DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_PreOrderDeadline_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Dummy demand
        demand = self.set_up_demand()

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
        supply = self.set_up_supply(
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

        # Match
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand
        )

        # Match ID, set by system when sending message
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

        # Connect user
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='PRE_ORDER_DEADLINE',
            target_body_params_func=self.get_target_body_params
        )
        self.assert_value(
            datas.\
                DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class DiscussWSellerDiscussConfirmInterestTest_MatchClosed_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()

        # Set user's name
        self.user.name = 'Kevin Ng'
        self.user.save()

        # Dummy supply
        supply = self.set_up_supply()

        # Dummy demand
        demand = self.set_up_demand()

        # Match - closed
        match = relmods.Match.objects.create(
            supply=supply,
            demand=demand,
            closed=timezone.now()
        )

        # Match ID, set by system when sending message
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__MATCH_ID__ID,
            value_id=match.id,
            inbound=False
        )

    def test_choose_any_option(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )