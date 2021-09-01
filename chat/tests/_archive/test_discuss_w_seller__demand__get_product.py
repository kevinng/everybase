from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWSellerDemandGetProductTest(ChatTest):
    def setUp(self):
        super().setUp(intents.DISCUSS_W_SELLER, messages.DEMAND__GET_PRODUCT)

    def test_enter_product(self):
        input = 'nitrile gloves'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DEMAND__GET_COUNTRY_STATE
        )
        self.assert_value(
            datas.PRODUCT,
            value_string=input
        )