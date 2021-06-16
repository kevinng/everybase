from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetPacking_ReadyOTG_UnknownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'ready/OTG' in an earlier step
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__READY_OTG
        )
        # User entered a string that does not match any known product
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.NEW_SUPPLY__SUPPLY__GET_PRODUCT__PRODUCT_TYPE__STRING,
            'BWwVWfauU29canbQmTcV' # String unlikely to match a known product
        )

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_UNKNOWN_PACKING
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING,
            value_string=input
        )

class NewSupplySupplyGetPacking_ReadyOTG_KnownPacking_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'ready/OTG' in an earlier step
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

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_READY_OTG_KNOWN_PACKING
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING,
            value_string=input
        )

class NewSupplySupplyGetPacking_PreOrder_UnknownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'pre-order' in an earlier step
        self.set_up_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__CHOICE,
            datas.NEW_SUPPLY__SUPPLY__GET_AVAILABILITY__AVAILABILITY__PRE_ORDER
        )

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
        self.assert_value(
            datas.NEW_SUPPLY__SUPPLY__GET_PACKING__PACKING__STRING,
            value_string=input
        )