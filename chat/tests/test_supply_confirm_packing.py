from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewSupplyConfirmPacking_ReadyOTG_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY, 
            messages.SUPPLY__CONFIRM_PACKING,
            texts.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING,
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class NewSupplyConfirmPacking_PreOrder_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__CONFIRM_PACKING,
            texts.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PACKING
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')