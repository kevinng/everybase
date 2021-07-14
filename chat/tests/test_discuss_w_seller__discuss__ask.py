from relationships import models as relmods
from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption
from chat.libraries.constants import intents, messages, datas
from chat.libraries.classes.chat_test import ChatTest

class DiscussWSellerDiscussAskTest(ChatTest):
    def setUp(self):
        super().setUp(
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__ASK
        )
    
    def test_get_question(self):
        match = self.setup_match(False, SupplyAvailabilityOption.OTG)

        input = 'Can you do OEM?'
        self.receive_reply_assert(
            input,
            intents.DISCUSS_W_SELLER,
            messages.DISCUSS__THANK_YOU
        )

        # There should be only 1
        qna = relmods.QuestionAnswerPair.objects.get(match=match.id)

        self.assert_value(
            datas.QUESTION,
            value_string=input
        )

        self.assertEqual(qna.questioner.id, self.user.id)
        self.assertEqual(qna.answerer.id, self.user_2.id)
        self.assertIsNotNone(qna.asked)
        self.assertIsNotNone(qna.question_captured_value)