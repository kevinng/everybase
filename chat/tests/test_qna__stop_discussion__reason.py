from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class QNAStopDiscussionReasonTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(
            intents.QNA,
            messages.STOP_DISCUSSION__REASON
        )

class QNAStopDiscussionReason_Normal_Test(QNAStopDiscussionReasonTest):
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        self.setup_qna()

    def test_any_input(self):
        input = 'hello world'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.STOP_DISCUSSION__THANK_YOU
        )
        self.assert_value(
            datas.STOP_DISCUSSION__REASON,
            value_string=input
        )

class QNAStopDiscussionReason_MatchClosed_Test(QNAStopDiscussionReasonTest):
    def setUp(self):
        super().setUp()
        self.setup_match(False, SupplyAvailabilityOption.OTG, True)
        self.setup_qna()

    def test_any_input(self):
        self.receive_reply_assert(
            '1',
            intents.MENU,
            messages.MENU
        )