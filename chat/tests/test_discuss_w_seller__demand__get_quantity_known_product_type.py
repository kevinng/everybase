from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest

class DiscussWSellerGetQuantityKnownProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )

        # User entered a product a product that's known in our database in
        # a previous step. Plural name is used in response template body of a
        # yes outcome.
        # Note: we're not performing numeric validation for now
        _, _, kw = self.set_up_product_type(uom_name='jar')
        self.set_up_data_value(
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRODUCT,
            datas.DISCUSS_W_SELLER__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def test_any_input(self):
        target = '500 jars'
        self.receive_reply_assert(
            '500 jars',
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.\
    DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__STRING,
            target
        )

    ##### Tests for old handler with numeric validation #####

    # def test_enter_bad_value(self):
    #     self.receive_reply_assert(
    #         'hello',
    #         intents.DISCUSS_W_SELLER,
    #         messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
    #         target_body_intent_key=intents.NO_INTENT,
    #         target_body_message_key=messages.DO_NOT_UNDERSTAND_NUMBER
    #     )

    # def enter_quantity(self, input, target):
    #     self.receive_reply_assert(
    #         input,
    #         intents.DISCUSS_W_SELLER,
    #         messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
    #     )
    #     self.assert_value(
    #         datas.\
    # DISCUSS_W_SELLER__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
    #         value_float=target
    #     )

    # def test_enter_quantity_1(self):
    #     self.enter_quantity('40', 40)

    # def test_enter_quantity_2(self):
    #     self.enter_quantity('10.5', 10.5)