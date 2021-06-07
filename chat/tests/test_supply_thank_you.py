from chat.tests import utils
from chat.libraries import intents, messages, datas

class SupplyThankYouTest(utils.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)
    
    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('10', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)

    def test_choose_non_choice_with_number(self):
        self.receive_reply_assert('hello', intents.NEW_SUPPLY, messages.SUPPLY__THANK_YOU)

    def test_choose_new_supply_with_number(self):
        self.receive_reply_assert('1',
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )

    def test_choose_new_supply_with_text(self):
        self.receive_reply_assert('find buyers',
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            datas.MENU__MENU__OPTION__FIND_BUYER
        )