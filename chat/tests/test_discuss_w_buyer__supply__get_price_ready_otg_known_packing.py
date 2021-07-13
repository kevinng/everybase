from chat.libraries.test_funcs.supply_availability_options import SupplyAvailabilityOption
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWBuyerGetPriceReadyOTGKnownPackingTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_BUYER,
            messages.SUPPLY__GET_PRICE_READY_OTG_KNOWN_PACKING
        )
        self.setup_match(False, SupplyAvailabilityOption.OTG)

    def test_get_price(self):
        input = 'USD 20'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__ASK,
            target_body_variation_key='SELLING'
        )
        self.assert_value(
            datas.PRICE,
            value_string=input
        )