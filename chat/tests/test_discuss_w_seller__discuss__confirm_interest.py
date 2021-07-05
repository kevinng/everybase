from urllib.parse import urljoin
from django.urls import reverse

from everybase import settings

from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import (MessageHandlerTest,
    SupplyAvailabilityOption)
from chat.libraries.utilities.connect import connect

from relationships import models as relmods

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
            messages.DISCUSS__CONFIRM_INTEREST
        )

class DiscussWSellerDiscussConfirmInterestTest_No_Buying_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG)

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__CONFIRM
        )
        self.assert_value(
            datas.CONFIRM_INTEREST,
            value_string=datas.CONFIRM_INTEREST__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class DiscussWSellerDiscussConfirmInterestTest_NotConnected_Yes_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_DETAILS
        )
        self.assert_value(
            datas.CONFIRM_INTEREST,
            value_string=datas.CONFIRM_INTEREST__YES
        )

class DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_OTG_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.OTG)
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        def get_params():
            """Helper function to render the template with the WhatsApp URL
            after it has been generated by the handler.
            """
            whatsapp = relmods.PhoneNumberType.objects.get(id=1) # WhatsApp
            hash = relmods.PhoneNumberHash.objects.get(
                user=self.user,
                phone_number=self.user_2_ph,
                phone_number_type=whatsapp
            )
            whatsapp_url = urljoin(settings.BASE_URL,
                reverse('chat_root:whatsapp', kwargs={ 'id': hash.id }))

            return { 'whatsapp_url': whatsapp_url }

        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='OTG',
            target_body_params_func=get_params
        )
        self.assert_value(
            datas.CONFIRM_INTEREST,
            value_string=datas.CONFIRM_INTEREST__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_PreOrderDuration_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.PRE_ORDER_DURATION)
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        def get_params():
            """Helper function to render the template with the WhatsApp URL
            after it has been generated by the handler.
            """
            whatsapp = relmods.PhoneNumberType.objects.get(id=1) # WhatsApp
            hash = relmods.PhoneNumberHash.objects.get(
                user=self.user,
                phone_number=self.user_2_ph,
                phone_number_type=whatsapp
            )
            whatsapp_url = urljoin(settings.BASE_URL,
                reverse('chat_root:whatsapp', kwargs={ 'id': hash.id }))

            return { 'whatsapp_url': whatsapp_url }

        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='PRE_ORDER_DURATION',
            target_body_params_func=get_params
        )
        self.assert_value(
            datas.CONFIRM_INTEREST,
            value_string=datas.CONFIRM_INTEREST__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

class DiscussWSellerDiscussConfirmInterestTest_Connected_Yes_PreOrderDeadline_Test(
    DiscussWSellerDiscussConfirmInterestTest):
    def setUp(self):
        super().setUp()
        self.setup_buyer(SupplyAvailabilityOption.PRE_ORDER_DEADLINE)
        connect(self.user, self.user_2)

    def choose_yes(self, input):
        def get_params():
            """Helper function to render the template with the WhatsApp URL
            after it has been generated by the handler.
            """
            whatsapp = relmods.PhoneNumberType.objects.get(id=1) # WhatsApp
            hash = relmods.PhoneNumberHash.objects.get(
                user=self.user,
                phone_number=self.user_2_ph,
                phone_number_type=whatsapp
            )
            whatsapp_url = urljoin(settings.BASE_URL,
                reverse('chat_root:whatsapp', kwargs={ 'id': hash.id }))

            return { 'whatsapp_url': whatsapp_url }

        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED,
            target_body_variation_key='PRE_ORDER_DEADLINE',
            target_body_params_func=get_params
        )
        self.assert_value(
            datas.CONFIRM_INTEREST,
            value_string=datas.CONFIRM_INTEREST__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')