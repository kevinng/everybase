from chat.libraries import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerStillInterestedThankYouTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.STILL_INTERESTED__THANK_YOU,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_new_supply(self, input):
        self.receive_reply_assert(input,
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
        self.receive_reply_assert(input,
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

    def test_learn_more(self):
        self.receive_reply_assert(
            '3', # Only number option available
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE
        )
        self.assert_value(
            datas.MENU__MENU__OPTION__CHOICE,
            value_string=datas.MENU__MENU__OPTION__LEARN_MORE
        )