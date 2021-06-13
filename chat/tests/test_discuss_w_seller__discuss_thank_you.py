from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class DiscussWSellerDiscussThankYouTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__THANK_YOU,
            name='Kevin Ng'
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.MENU,
            messages.MENU,
            texts.MENU__MENU
        )
    
    # def test_choose_non_choice_with_number(self):
    #     self.choose_non_choice('10')

    # def test_choose_non_choice_with_text(self):
    #     self.choose_non_choice('hello')

    def choose_new_supply(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            value_string=datas.MENU__MENU__OPTION__FIND_BUYER
        )

    def test_choose_new_supply_with_number(self):
        self.choose_new_supply('1')

    def test_choose_new_supply_with_text(self):
        self.choose_new_supply('find buyers')

    def choose_new_demand(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            value_string=datas.MENU__MENU__OPTION__FIND_SELLER
        )

    def test_choose_new_demand_with_number(self):
        self.choose_new_demand('2')

    def test_choose_new_demand_with_text(self):
        self.choose_new_demand('find sellers')