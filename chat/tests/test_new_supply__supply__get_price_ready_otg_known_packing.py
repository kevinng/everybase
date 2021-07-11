from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class NewSupplyGetPriceReadyOTGKnownPackingTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.NEW_SUPPLY,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
    
    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.NEW_SUPPLY,
            messages.SUPPLY__THANK_YOU
        )
        self.assert_value(
            datas.PRICE,
            value_string=input
        )