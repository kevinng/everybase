from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest
from chat.tests import texts

class NewSupplySupplyConfirmPacking_ReadyOTG_KnownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        # User chose ready/OTG in a previous step.
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )
        # User entered a product a product that's known in our database in
        # a previous step. Plural name is used in response template body of a
        # yes outcome.
        _, _, kw = self.set_up_product_type(
            uom_plural_name='cartons')
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY, 
            messages.SUPPLY__CONFIRM_PACKING,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
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
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES
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
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class NewSupplySupplyConfirmPacking_ReadyOTG_UnknownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        # User chose ready/OTG in a previous step.
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )

        # User entered a product a product that's unknown in our database in
        # a previous step.
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'mCGYaiIbemoD5R552EC0' # Unlikely string to match any known product
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY, 
            messages.SUPPLY__CONFIRM_PACKING,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES
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
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class NewSupplySupplyConfirmPacking_PreOrder_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__CONFIRM_PACKING)
        # User chose pre-order in a previous step.
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )
        # User entered a product a product that's unknown in our database in
        # a previous step.
        _, _, kw = self.set_up_product_type(
            'Product X'
        )
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'hello world' # Not matching product name
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__CONFIRM_PACKING,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
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
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__YES
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
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__CHOICE,
            value_string=datas.NEW_SUPPLY__SUPPLY__CONFIRM_PACKING__CORRECT__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')