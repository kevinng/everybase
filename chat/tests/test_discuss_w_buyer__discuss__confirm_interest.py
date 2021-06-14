import datetime, pytz
from chat.libraries import intents, messages, datas, model_utils
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts
from relationships import models as relmods
from common import models as commods
from payments import models as paymods

class DiscussWBuyerDiscussConfirmInterestTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            None
        )

        # User 1 ID, set by system when sending this message to the user
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_1__ID,
            value_id=self.user.id,
            inbound=False
        )

        # User 2, set by system when sending this message to the user
        self.user_2, _ = self.create_user_phone_number(
            'Test Seller', '23456', '2345678901')
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__USER_2__ID,
            value_id=self.user_2.id,
            inbound=False
        )

class DiscussWBuyerDiscussConfirmInterestTest_NotConnected_YesNo_Test(
    DiscussWBuyerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()

        # Demand and relevant models, and demand ID set by the system when
        # sending this message to the user
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
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__DEMAND__ID,
            value_id=demand.id,
            inbound=False
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            texts.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_DETAILS,
            texts.DISCUSS_W_BUYER__DISCUSS__CONFIRM_DETAILS
        )
        self.assert_value(
            datas.\
                DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.STILL_INTERESTED__CONFIRM,
            texts.DISCUSS_W_BUYER__STILL_INTERESTED__CONFIRM
        )
        self.assert_value(
            datas.\
                DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class DiscussWBuyerDiscussConfirmInterestTest_Connected_Yes_OTG_Test(
    DiscussWBuyerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Supply and relevant models, and supply ID set by the system when
        # sending this message to the user
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
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID,
            value_id=supply.id,
            inbound=False
        )

        # Connect user
        model_utils.connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ALREADY_CONNECTED,
            texts.DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED__OTG
        )
        self.assert_value(
            datas.\
                DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class \
DiscussWBuyerDiscussConfirmInterestTest_Connected_Yes_PreOrderDuration_Test(
    DiscussWBuyerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Supply and relevant models, and supply ID set by the system when
        # sending this message to the user
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
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID,
            value_id=supply.id,
            inbound=False
        )

        # Connect user
        model_utils.connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ALREADY_CONNECTED,
        texts.DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED__PRE_ORDER_DURATION
        )
        self.assert_value(
            datas.\
                DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class \
DiscussWBuyerDiscussConfirmInterestTest_Connected_Yes_PreOrderDeadline_Test(
    DiscussWBuyerDiscussConfirmInterestTest):
    """Supply use default OTG settings"""
    def setUp(self):
        super().setUp()

        # Supply and relevant models, and supply ID set by the system when
        # sending this message to the user
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
        self.set_up_data_value(
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID,
            value_id=supply.id,
            inbound=False
        )

        # Connect user
        model_utils.connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ALREADY_CONNECTED,
        texts.DISCUSS_W_BUYER__DISCUSS__ALREADY_CONNECTED__PRE_ORDER_DEADLINE
        )
        self.assert_value(
            datas.\
                DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__CHOICE,
            value_string=\
            datas.DISCUSS_W_BUYER__DISCUSS__CONFIRM_INTEREST__INTERESTED__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')