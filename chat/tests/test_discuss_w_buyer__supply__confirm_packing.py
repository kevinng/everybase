from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DisucssWBuyerSupplyConfirmPacking_ReadyOTG_KnownPacking_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__CONFIRM_PACKING)
        # User chose ready/OTG in a previous step.
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG
        )
        # User entered a product a product that's known in our database in
        # a previous step. Plural name is used in response template body of a
        # yes outcome.
        _, _, kw = self.setup_product_type(
            uom_plural_name='cartons')
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER, 
            messages.SUPPLY__CONFIRM_PACKING,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('3')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello')

    def choose_yes(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class DisucssWBuyerSupplyConfirmPacking_ReadyOTG_UnknownPacking_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__CONFIRM_PACKING)
        # User chose ready/OTG in a previous step.
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG
        )

        # User entered a product a product that's unknown in our database in
        # a previous step.
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'mCGYaiIbemoD5R552EC0' # Unlikely string to match any known product
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER, 
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
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')

class DisucssWBuyerSupplyConfirmPacking_PreOrder_Test(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_BUYER, messages.SUPPLY__CONFIRM_PACKING)
        # User chose pre-order in a previous step.
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__PRE_ORDER
        )
        # User entered a product a product that's unknown in our database in
        # a previous step.
        _, _, kw = self.setup_product_type(
            'Product X'
        )
        self.setup_data_value(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
            'hello world' # Not matching product name
        )

    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
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
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__YES
        )

    def test_choose_yes_with_number(self):
        self.choose_yes('1')

    def test_choose_yes_with_text(self):
        self.choose_yes('yes')

    def choose_no(self, input):
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PACKING
        )
        self.assert_value(
            datas.CONFIRM_PACKING,
            value_string=datas.CONFIRM_PACKING__NO
        )

    def test_choose_no_with_number(self):
        self.choose_no('2')

    def test_choose_no_with_text(self):
        self.choose_no('no')