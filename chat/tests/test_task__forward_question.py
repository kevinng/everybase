from chat.tasks.forward_question import forward_question
from chat.libraries.classes.chat_test import ChatTest
from chat.libraries.constants import intents, messages

from chat.libraries.test_funcs.supply_availability_options import \
    SupplyAvailabilityOption

class TaskForwardQuestionTest(ChatTest):
    fixtures = [
        'setup/common__country.json',
        'setup/20210528__payments__currency.json',
        'setup/20210527__relationships__availability.json',
        'setup/20210527__relationships__user.json',
        'setup/20210527__relationships__phonenumber.json',
        'setup/20210527__relationships__phonenumbertype.json'
    ]

    def test_answer_not_ready(self):
        self.setup_match(False, SupplyAvailabilityOption.OTG)
        qna = self.setup_qna(question_readied=False)
        msg = forward_question(qna, True)
        self.assertEqual(msg, None)

    def test_run_selling(self):
        self.setup_match(False, SupplyAvailabilityOption.OTG)

        # answering=True because I'm answering question (as a seller), so I'm
        # being forwarded (i.e., receiving) the message.
        qna = self.setup_qna(
            answering=True,
            answered=False,
            question_readied=True
        )
        
        msg = forward_question(qna, True)

        self.send_assert(
            msg.body,
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='SELLING'
        )
        self.assertNotEqual(
            qna.question_forwarded,
            None
        )

    def test_run_buying(self):
        self.setup_match(True, SupplyAvailabilityOption.OTG)

        # answering=True because I'm answering question (as a buyer), so I'm
        # being forwarded (i.e., receiving) the message.
        qna = self.setup_qna(
            answering=True,
            answered=False,
            question_readied=True
        )
        
        msg = forward_question(qna, True)

        self.send_assert(
            msg.body,
            intents.QNA,
            messages.YOUR_QUESTION,
            target_body_variation_key='BUYING'
        )
        self.assertNotEqual(
            qna.question_forwarded,
            None
        )