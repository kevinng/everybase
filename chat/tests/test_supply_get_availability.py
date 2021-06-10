from django.template.loader import render_to_string
from chat.libraries import intents, messages, datas, chat_flow_test

class NewSupplyGetAvailabilityTest(chat_flow_test.ChatFlowTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_AVAILABILITY)

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            render_to_string('chat/DO_NOT_UNDERSTAND_OPTION.txt')
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')
    
    def choose_ready_otg(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_READY_OTG
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=\
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def test_choose_ready_otg_with_number(self):
        self.choose_ready_otg('1')

    def test_choose_ready_otg_with_text_1(self):
        self.choose_ready_otg('ready')

    def test_choose_ready_otg_with_text_2(self):
        self.choose_ready_otg('otg')

    def choose_preorder(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_COUNTRY_STATE_PRE_ORDER
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            value_string=\
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_choose_preorder_with_number(self):
        self.choose_preorder('2')

    def test_choose_preorder_with_text(self):
        self.choose_preorder('pre order')