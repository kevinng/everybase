from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class NewDemandGetQuantityKnownProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )

        # User entered a product a product that's known in our database in
        # a previous step. Plural name is used in response template body of a
        # yes outcome.
        # Note: we're not performing numeric validation for now
        _, _, kw = self.setup_product_type(uom_name='jar')
        self.setup_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.PRODUCT,
            kw.keyword
        )

    def test_any_input(self):
        target = '500 jars'
        self.receive_reply_assert(
            '500 jars',
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.QUANTITY,
            target
        )

    ##### Tests for old handler which validates numeric inputs #####

    # def test_enter_bad_value(self):
    #     self.receive_reply_assert(
    #         'hello',
    #         intents.NEW_DEMAND,
    #         messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
    #         target_body_intent_key=intents.NO_INTENT,
    #         target_body_message_key=messages.DO_NOT_UNDERSTAND_NUMBER
    #     )

    # def enter_quantity(self, input, target):
    #     self.receive_reply_assert(
    #         input,
    #         intents.NEW_DEMAND,
    #         messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
    #     )
    #     self.assert_value(
    #         datas.\
    #     NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
    #         value_float=target
    #     )

    # def test_enter_quantity_1(self):
    #     self.enter_quantity('40', 40)

    # def test_enter_quantity_2(self):
    #     self.enter_quantity('10.5', 10.5)