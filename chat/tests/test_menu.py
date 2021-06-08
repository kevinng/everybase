from chat.tests import utils
from chat.libraries import intents, messages, datas

class MenuTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.MENU, messages.MENU, None)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('10', intents.MENU, messages.MENU)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('hello', intents.MENU, messages.MENU)

    def choose_new_supply(self, input):
        self.receive_reply_assert(input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )

    def test_choose_new_supply_with_number(self):
        self.choose_new_supply('1')

    def test_choose_new_supply_with_text(self):
        self.choose_new_supply('find buyers')

    def choose_new_demand(self, input):
        self.receive_reply_assert(input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_SELLER
        )

    def test_choose_new_demand_with_number(self):
        self.choose_new_demand('2')

    def test_choose_new_demand_with_text(self):
        self.choose_new_demand('find sellers')