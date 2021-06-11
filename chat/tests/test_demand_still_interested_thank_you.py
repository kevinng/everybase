from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class DemandStillInterestedThankYouTest(MessageHandlerTest):
    
    def setUp(self):
        super().setUp(intents.DISCUSS_W_SELLER,
        messages.STILL_INTERESTED__THANK_YOU)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU,
            texts.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_new_supply(self, input):
        self.receive_reply_assert(input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            texts.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__CHOICE,
            value_string=\
        datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__FIND_BUYER
        )

    def test_choose_new_supply_with_number(self):
        self.choose_new_supply('1')

    def test_choose_new_supply_with_text(self):
        self.choose_new_supply('find buyers')

    def choose_new_demand(self, input):
        self.receive_reply_assert(input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            texts.DEMAND__GET_PRODUCT
        )
        self.assert_value(
            datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__CHOICE,
            value_string=\
        datas.DISCUSS_W_SELLER__STILL_INTERESTED__THANK_YOU__OPTION__FIND_SELLER
        )

    def test_choose_new_demand_with_number(self):
        self.choose_new_demand('2')

    def test_choose_new_demand_with_text(self):
        self.choose_new_demand('find sellers')