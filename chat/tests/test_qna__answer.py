from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.message_handler_test import MessageHandlerTest, SupplyAvailabilityOption

class QNAAnswerTest(MessageHandlerTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json'
    ]

    def setUp(self):
        super().setUp(intents.QNA, messages.ANSWER)
        self.setup_buyer(SupplyAvailabilityOption.OTG)
        self.setup_qna()

    def test_enter_answer(self):
        input = 'Yes, we can.'
        self.receive_reply_assert(
            input,
            intents.QNA,
            messages.ANSWER__THANK_YOU
        )
        self.assert_value(
            datas.ANSWER,
            value_string=input
        )

        # TODO: be sure that QNA's timestamp has been updated

# class QNAAnswer_Buying_OTG_Test(QNAAnswerTest):
#     def setUp(self):
#         super().setUp()

#         # TODO Setup functions should be in message handlers
#         match = setup_buyer(self, supply_type=OTG)
#         setup_qna(self, match, answering=True, answered=False)

#     def test_enter_answer(self):

#         # TODO this function call seems to be wrong
#         self._test_enter_answer('BUYING__OTG__INITIAL')

# class QNAAnswer_Buying_PreOrderDeadline_Test(QNAAnswerTest):
#     def setUp(self):
#         super().setUp()
#         match = setup_buyer(self, supply_type=PRE_ORDER_DEADLINE)
#         setup_qna(self, match, answering=True, answered=False)

#     def test_enter_answer(self):
#         self._test_enter_answer('BUYING__PRE_ORDER_DEADLINE__INITIAL')

# class QNAAnswer_Buying_PreOrderDuration_Test(QNAAnswerTest):
#     def setUp(self):
#         super().setUp()
#         match = setup_buyer(self, supply_type=PRE_ORDER_DURATION)
#         setup_qna(self, match, answering=True, answered=False)

#     def test_enter_answer(self):
#         self._test_enter_answer('BUYING__PRE_ORDER_DURATION__INITIAL')

# class QNAAnswer_Selling_Test(QNAAnswerTest):
#     def setUp(self):
#         super().setUp()
#         match = setup_seller(self)
#         setup_qna(self, match, answering=True, answered=False)

#     def test_enter_answer(self):
#         self._test_enter_answer('SELLING__INITIAL')