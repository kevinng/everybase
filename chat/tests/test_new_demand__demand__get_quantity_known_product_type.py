from chat.tests import texts
from chat.libraries import intents, messages, datas
from chat.libraries.message_handler_test import MessageHandlerTest

class NewDemandGetQuantityKnownProductTest(MessageHandlerTest):
    def setUp(self):
        super().setUp(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE
        )
        # User entered a product a product that's known in our database in
        # a previous step. Plural name is used in response template body of a
        # yes outcome.
        _, _, kw = self.set_up_product_type(uom_name='jar')
        self.set_up_data_value(
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRODUCT,
            datas.NEW_DEMAND__DEMAND__GET_PRODUCT__PRODUCT_TYPE__STRING,
            kw.keyword
        )

    def test_enter_bad_value(self):
        self.receive_reply_assert(
            'hello',
            intents.NEW_DEMAND,
            messages.DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_NUMBER
        )

    def enter_quantity(self, input, target):
        self.receive_reply_assert(
            input,
            intents.NEW_DEMAND,
            messages.DEMAND__GET_PRICE_KNOWN_PRODUCT_TYPE
        )
        self.assert_value(
            datas.\
        NEW_DEMAND__DEMAND__GET_QUANTITY_KNOWN_PRODUCT_TYPE__QUANTITY__NUMBER,
            value_float=target
        )

    def test_enter_quantity_1(self):
        self.enter_quantity('40', 40)

    def test_enter_quantity_2(self):
        self.enter_quantity('10.5', 10.5)