from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewSupplySupplyGetPacking_ReadyOTG_UnknownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'ready/OTG' in an earlier step
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__READY_OTG
        )
        # User entered a string that does not match any known product
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
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
            datas.PACKING,
            value_string=input
        )

class NewSupplySupplyGetPacking_ReadyOTG_KnownPacking_Test(MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'ready/OTG' in an earlier step
        self.setup_data_value(
            intents.NEW_SUPPLY,
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
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRODUCT,
            datas.PRODUCT,
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
            datas.PACKING,
            value_string=input
        )

class NewSupplySupplyGetPacking_PreOrder_UnknownPacking_Test(
    MessageHandlerTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PACKING)
        # User chose 'pre-order' in an earlier step
        self.setup_data_value(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY,
            datas.AVAILABILITY,
            datas.AVAILABILITY__PRE_ORDER
        )

    def test_receive_packing(self):
        input = '100 pieces in 1 box'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_QUANTITY_PRE_ORDER
        )
        self.assert_value(
            datas.PACKING,
            value_string=input
        )