from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class NewSupplySupplyGetProductTest(ChatTest):
    def setUp(self):
        super().setUp(intents.NEW_SUPPLY, messages.SUPPLY__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_AVAILABILITY
        )
        self.assert_value(
            datas.PRODUCT,
            value_string=input
        )