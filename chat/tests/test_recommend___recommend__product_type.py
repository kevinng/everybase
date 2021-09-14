from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class TestBase():
    def choose_non_choice(self, input):
        self.receive_reply_assert(
            input,
            intents.RECOMMEND,
            messages.RECOMMEND__PRODUCT_TYPE,
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

    def _test_yes(self, is_buying):
        self.receive_reply_assert(
            '1',
            intents.RECOMMEND,
            messages.RECOMMEND__DETAILS,
            target_body_variation_key='BUY' if is_buying else 'SELL'
        )
        self.assert_value(
            datas.RECOMMEND__PRODUCT_TYPE,
            value_string=datas.RECOMMEND__PRODUCT_TYPE__YES
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_product_type_choice,
            datas.RECOMMEND__PRODUCT_TYPE__YES
        )

    def test_not_now(self):
        self.receive_reply_assert(
            '2',
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_NOW_CONFIRMED,
            target_body_variation_key='REGISTERED'
        )
        self.assert_value(
            datas.RECOMMEND__PRODUCT_TYPE,
            value_string=datas.RECOMMEND__PRODUCT_TYPE__NOT_NOW
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_product_type_choice,
            datas.RECOMMEND__PRODUCT_TYPE__NOT_NOW
        )

    def _test_not_interested(self, is_buying):
        self.receive_reply_assert(
            '3',
            intents.RECOMMEND,
            messages.RECOMMEND__NOT_INTERESTED_CONFIRM,
            target_body_variation_key='REGISTERED'
        )
        self.assert_value(
            datas.RECOMMEND__PRODUCT_TYPE,
            value_string=datas.RECOMMEND__PRODUCT_TYPE__NO
        )
        self.assertEqual(
            self.user.current_recommendation.recommend_product_type_choice,
            datas.RECOMMEND__PRODUCT_TYPE__NO
        )

class RECOMMEND___RECOMMEND__PRODUCT_TYPE___Buy___Test(TestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__PRODUCT_TYPE,
            is_buying=True
        )

    def test_yes(self):
        self._test_yes(True)

    def test_not_interested(self):
        self._test_not_interested(True)

class RECOMMEND___RECOMMEND__PRODUCT_TYPE___Sell___Test(TestBase, ChatTest):
    def setUp(self):
        super().setUp(
            intents.RECOMMEND,
            messages.RECOMMEND__PRODUCT_TYPE,
            is_buying=False
        )

    def test_yes(self):
        self._test_yes(False)

    def test_not_interested(self):
        self._test_not_interested(False)