from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class TestBase():
    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            target_body_intent_key=intents.NO_INTENT,
            target_body_message_key=messages.DO_NOT_UNDERSTAND_OPTION
        )
        self.assert_value(
            datas.INVALID_CHOICE,
            value_string=input
        )

    def test_choose_non_choice_with_number(self):
        self.choose_non_choice('10')

    def test_choose_non_choice_with_text(self):
        self.choose_non_choice('hello world')

    def test_i_am_direct(self):
        self.receive_reply_assert(
            '1',
            intents.RECOMMEND,
            messages.TALK_TO_HUMAN__CONFIRMED,
            target_body_variation_key='REGISTERED'
        )
        self.assert_value(
            datas.RECOMMEND__DETAILS,
            value_string=datas.RECOMMEND__DETAILS__DIRECT
        )

    def _test_i_can_find(self, is_buying=True):
        self.receive_reply_assert(
            '2',
            intents.RECOMMEND,
            messages.RECOMMEND__I_CAN_FIND,
            target_body_variation_key='BUY' if is_buying else 'SELL'
        )
        self.assert_value(
            datas.RECOMMEND__DETAILS,
            value_string=datas.RECOMMEND__DETAILS__CAN_FIND
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_details_choice,
            datas.RECOMMEND__DETAILS__CAN_FIND
        )

    def test_not_now(self):
        self.receive_reply_assert(
            '3',
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_NOW_CONFIRM,
            target_body_variation_key='REGISTERED'
        )
        self.assert_value(
            datas.RECOMMEND__DETAILS,
            value_string=datas.RECOMMEND__DETAILS__NOT_NOW
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_details_choice,
            datas.RECOMMEND__DETAILS__NOT_NOW
        )

    def test_not_interested(self):
        self.receive_reply_assert(
            '4',
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS__NOT_INTERESTED
        )
        self.assert_value(
            datas.RECOMMEND__DETAILS,
            value_string=datas.RECOMMEND__DETAILS__NOT_INTERESTED
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_details_choice,
            datas.RECOMMEND__DETAILS__NOT_INTERESTED
        )

class RECOMMEND___RECOMMEND__DETAILS___Buy___Test(TestBase, ChatTest):
    def setUp(self):
        super().setUp(intents.RECOMMEND, messages.RECOMMEND__DETAILS)

    def test_i_can_find(self):
        self._test_i_can_find()

class RECOMMEND___RECOMMEND__DETAILS___Sell___Test(TestBase, ChatTest):
    def setUp(self):
        super().setUp(intents.RECOMMEND, messages.RECOMMEND__DETAILS,
            is_buying=False
        )

    def test_i_can_find(self):
        self._test_i_can_find(False)