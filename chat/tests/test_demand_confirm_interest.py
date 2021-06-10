from django.template.loader import render_to_string
from chat.libraries import intents, messages, datas, model_utils, chat_flow_test

class DemandConfirmInterestTest(chat_flow_test.ChatFlowTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            None
        )
        pt, _, _ = self.set_up_product_type()
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
            datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__PRODUCT_TYPE__ID,
            value_id=pt.id,
            inbound=False
        )
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_1__ID,
            value_id=self.user.id,
            inbound=False
        )
        self.user_2, _ = self.create_user_phone_number('Test Seller', '23456',
            '2345678901')
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__USER_2__ID,
            value_id=self.user_2.id,
            inbound=False
        )

        supply = self.set_up_supply()
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            data_key=\
                datas.DISCUSS_W_SELLER__DISCUSS__CONFIRM_INTEREST__SUPPLY__ID,
            value_id=supply.id,
            inbound=False
        )

class DemandConfirmInterest_NotConnected_Test(DemandConfirmInterestTest):
    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            render_to_string('chat/DO_NOT_UNDERSTAND_OPTION.txt')
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

class DemandConfirmInterest_Connected_Test(DemandConfirmInterestTest):
    def setUp(self):
        super().setUp()

        # Connect user
        model_utils.connect(self.user, self.user_2)

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ALREADY_CONNECTED
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