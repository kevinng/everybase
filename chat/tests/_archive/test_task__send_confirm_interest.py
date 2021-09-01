from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.tasks.send_confirm_interests import send_confirm_interests
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import datas, intents, messages, methods

_fixtures = [
    'setup/20210527__relationships__user.json',
    'setup/20210527__relationships__availability.json',
    'setup/20210527__relationships__phonenumber.json',
    'setup/20210527__relationships__phonenumbertype.json',
    'setup/20210528__payments__currency.json',
    'setup/common__country.json'
]

class TaskSendConfirmInterestTest(ChatTest):
    fixtures = _fixtures

    def test_otg(self):
        match = self.setup_match(True, SupplyAvailabilityOption.OTG)
        
        send_confirm_interests(match.id, no_external_calls=True)
        match.refresh_from_db()

        self.send_assert(
            match.sent_buyer_confirm_interest_message.body,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            target_body_variation_key='OTG'
        )
        self.send_assert(
            match.sent_seller_confirm_interest_message.body,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            counter_party=True
        )

        self.assertIsNotNone(match.sent_buyer_confirm_interest)
        self.assertIsNotNone(match.sent_seller_confirm_interest)

    def test_pre_order_deadline(self):
        match = self.setup_match(
            True, SupplyAvailabilityOption.PRE_ORDER_DEADLINE)

        send_confirm_interests(match.id, no_external_calls=True)
        match.refresh_from_db()

        self.send_assert(
            match.sent_buyer_confirm_interest_message.body,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            target_body_variation_key='PRE_ORDER_DEADLINE'
        )
        self.send_assert(
            match.sent_seller_confirm_interest_message.body,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            counter_party=True
        )

        self.assertIsNotNone(match.sent_buyer_confirm_interest)
        self.assertIsNotNone(match.sent_seller_confirm_interest)

    def test_pre_order_duration(self):
        match = self.setup_match(
            True, SupplyAvailabilityOption.PRE_ORDER_DURATION)

        send_confirm_interests(match.id, no_external_calls=True)
        match.refresh_from_db()

        self.send_assert(
            match.sent_buyer_confirm_interest_message.body,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__CONFIRM_INTEREST,
            target_body_variation_key='PRE_ORDER_DURATION'
        )
        self.send_assert(
            match.sent_seller_confirm_interest_message.body,
            intents.DISCUSS_W_BUYER,
            messages.DISCUSS__CONFIRM_INTEREST,
            counter_party=True
        )

        self.assertIsNotNone(match.sent_buyer_confirm_interest)
        self.assertIsNotNone(match.sent_seller_confirm_interest)