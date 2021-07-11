from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class QNAStopDiscussionThankYouTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.STOP_DISCUSSION__THANK_YOU
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.STOP_DISCUSSION__THANK_YOU,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_new_supply(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__FIND_BUYERS
        )

    def test_choose_new_supply_with_number(self):
        self.choose_new_supply('1')

    def test_choose_new_supply_with_text(self):
        self.choose_new_supply('buyers')

    def choose_new_demand(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__FIND_SELLERS
        )

    def test_choose_new_demand_with_number(self):
        self.choose_new_demand('2')

    def test_choose_new_demand_with_text(self):
        self.choose_new_demand('sellers')

    def test_learn_more(self):
        self.receive_reply_assert(
            '3', # Only number option available
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE
        )
        self.assert_value(
            datas.MENU,
            value_string=datas.MENU__LEARN_MORE
        )