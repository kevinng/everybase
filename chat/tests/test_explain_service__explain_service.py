from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class ExplainService__ExplainService__Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.EXPLAIN_SERVICE, messages.EXPLAIN_SERVICE)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.EXPLAIN_SERVICE,
            messages.EXPLAIN_SERVICE,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
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
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            value_string=\
                datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_BUYER
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
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            value_string=\
                datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__FIND_SELLER
        )

    def test_choose_new_demand_with_number(self):
        self.choose_new_demand('2')

    def test_choose_new_demand_with_text(self):
        self.choose_new_demand('find sellers')

    def test_speak_human(self):
        self.receive_reply_assert(
            '3', # Only number option available
            intents.SPEAK_HUMAN,
            messages.CONFIRM_HUMAN
        )
        self.assert_value(
            datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__CHOICE,
            value_string=\
                datas.EXPLAIN_SERVICE__EXPLAIN_SERVICE__OPTION__SPEAK_HUMAN
        )